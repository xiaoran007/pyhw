#include <IOKit/IOKitLib.h>
#include <CoreFoundation/CoreFoundation.h>
#include <stdio.h>
#include <stdlib.h>

double get_cpu_max_frequency(void) {
    // https://github.com/fastfetch-cli/fastfetch/blob/dev/src/detection/cpu/cpu_apple.c
    io_registry_entry_t entryDevice = IOServiceGetMatchingService(MACH_PORT_NULL, IOServiceNameMatching("pmgr"));
    if (!entryDevice)
        return 0.0;

    if (!IOObjectConformsTo(entryDevice, "AppleARMIODevice")) {
        IOObjectRelease(entryDevice);
        return 0.0;
    }

    CFDataRef freqProperty = (CFDataRef)IORegistryEntryCreateCFProperty(entryDevice,
                                                                      CFSTR("voltage-states5-sram"),
                                                                      kCFAllocatorDefault,
                                                                      kNilOptions);

    double max_freq = 0.0;

    if (freqProperty && CFGetTypeID(freqProperty) == CFDataGetTypeID()) {
        CFIndex propLength = CFDataGetLength(freqProperty);
        if (propLength > 0 && propLength % sizeof(uint32_t) * 2 == 0) {
            uint32_t* pStart = (uint32_t*)CFDataGetBytePtr(freqProperty);
            uint32_t pMax = *pStart;

            // Iterate through frequency/voltage pairs to find maximum
            for (CFIndex i = 2; i < propLength / sizeof(uint32_t) && pStart[i] > 0; i += 2) {
                pMax = pMax > pStart[i] ? pMax : pStart[i];
            }

            if (pMax > 0) {
                // Convert to GHz based on value scale
                if (pMax > 100000000) // Frequency in Hz (M1-M3)
                    max_freq = (double)pMax / 1000000000.0;
                else // Frequency in kHz (M4 and later)
                    max_freq = (double)pMax / 1000000.0;
            }
        }
        CFRelease(freqProperty);
    }

    IOObjectRelease(entryDevice);
    return max_freq;
}

// Function to be called from Python
double get_apple_silicon_max_frequency(void) {
    return get_cpu_max_frequency();
}