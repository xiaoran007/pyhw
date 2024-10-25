import Foundation
import IOKit

func getGPUInfo() {
    // Create a matching dictionary for PCI devices
    let matchingDict = IOServiceMatching("IOPCIDevice")
    var iterator: io_iterator_t = 0

    // Get an iterator for all matching devices
    let result = IOServiceGetMatchingServices(kIOMasterPortDefault, matchingDict, &iterator)
    guard result == KERN_SUCCESS else {
        print("Failed to get matching services")
        return
    }

    var gpuNames = [String]()

    // Iterate over the matching devices
    var service = IOIteratorNext(iterator)
    while service != 0 {
        // Create an unmanaged reference to CF properties dictionary
        var properties: Unmanaged<CFMutableDictionary>?
        if IORegistryEntryCreateCFProperties(service, &properties, kCFAllocatorDefault, 0) == KERN_SUCCESS,
           let props = properties?.takeRetainedValue() as? [String: Any] {

            // Read the "model" property for the GPU name
            if let modelData = props["model"] as? Data,
               let modelName = String(data: modelData, encoding: .utf8) {
                gpuNames.append(modelName)
            }
        }

        // Release the current service object and move to the next
        IOObjectRelease(service)
        service = IOIteratorNext(iterator)
    }

    IOObjectRelease(iterator)

    // Print detected GPUs
    if gpuNames.isEmpty {
        print("No GPUs found.")
    } else {
        print("Detected GPUs:")
        for gpu in gpuNames {
            print("  GPU: \(gpu)")
        }
    }
}

getGPUInfo()