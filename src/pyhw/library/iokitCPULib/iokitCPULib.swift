import Foundation
import IOKit

@_cdecl("getPCoreFrequency")
public func getPCoreFrequency() -> Double {
    return getCPUFrequency(cpuType: "P-Core")
}

@_cdecl("getECoreFrequency")
public func getECoreFrequency() -> Double {
    return getCPUFrequency(cpuType: "E-Core")
}

private func getCPUFrequency(cpuType: String) -> Double {
    // First approach: Check CPU directly
    var iter: io_iterator_t = 0
    let result = IOServiceGetMatchingServices(kIOMasterPortDefault, IOServiceMatching("AppleARMCPU"), &iter)

    guard result == KERN_SUCCESS && iter != 0 else {
        return getCPUFrequencyFromPlatform(cpuType: cpuType)
    }

    defer {
        IOObjectRelease(iter)
    }

    var service = IOIteratorNext(iter)
    while service != 0 {
        defer {
            IOObjectRelease(service)
        }

        // Try to get frequency from different possible keys
        let keys = ["frequency", "clock-frequency", "max-clock-frequency",
                    cpuType.lowercased() + "-frequency",
                    cpuType.lowercased().replacingOccurrences(of: "-", with: "") + "-frequency"]

        for key in keys {
            if let data = IORegistryEntryCreateCFProperty(service, key as CFString, kCFAllocatorDefault, 0) {
                let number = data.takeUnretainedValue() as? NSNumber
                if let freq = number?.uint64Value, freq > 0 {
                    return Double(freq) / 1_000_000_000.0
                }
            }
        }

        service = IOIteratorNext(iter)
    }

    return getCPUFrequencyFromPlatform(cpuType: cpuType)
}

private func getCPUFrequencyFromPlatform(cpuType: String) -> Double {
    // Try to get from sysctl as fallback
    var mib = [CTL_HW, HW_CPU_FREQ]
    var size = MemoryLayout<UInt64>.size
    var freq: UInt64 = 0

    let result = sysctl(&mib, 2, &freq, &size, nil, 0)
    if result == 0 && freq > 0 {
        return Double(freq) / 1_000_000_000.0
    }

    // Last resort: try IOPlatformExpertDevice
    let service = IOServiceGetMatchingService(kIOMasterPortDefault, IOServiceMatching("IOPlatformExpertDevice"))
    guard service != 0 else {
        return 0.0
    }

    defer {
        IOObjectRelease(service)
    }

    // Try multiple path variations
    let keyPaths = [
        "CPU \(cpuType)",
        "cpu-\(cpuType.lowercased())",
        "cpu-\(cpuType.lowercased())-frequency",
        "cpu-info.\(cpuType.lowercased())-frequency",
        "device-frequencies.\(cpuType.lowercased())"
    ]

    for keyPath in keyPaths {
        if let data = IORegistryEntryCreateCFProperty(service, keyPath as CFString, kCFAllocatorDefault, 0) {
            let number = data.takeUnretainedValue() as? NSNumber
            if let freq = number?.uint64Value, freq > 0 {
                return Double(freq) / 1_000_000_000.0
            }
        }
    }

    // If all else fails, try a more comprehensive search through the registry
    print("Fallback to searching IORegistry for CPU frequency")
    return searchIORegistryForCPUFrequency(cpuType: cpuType)
}

private func searchIORegistryForCPUFrequency(cpuType: String) -> Double {
    var frequency: Double = 0.0

    func searchRegistry(service: io_registry_entry_t, depth: Int = 0) {
        if depth > 5 { return } // Limit recursion

        let properties = getServiceProperties(service)

        // Look for frequency-related properties
        for (key, value) in properties {
            let keyLower = key.lowercased()
            if (keyLower.contains("frequency") || keyLower.contains("clock")) &&
               (keyLower.contains(cpuType.lowercased()) || !keyLower.contains("core")) {
                if let number = value as? NSNumber, number.doubleValue > 0 {
                    let possibleFreq = number.doubleValue
                    // Assuming the frequency is either in Hz or MHz
                    if possibleFreq > 1_000_000_000 {
                        frequency = possibleFreq / 1_000_000_000.0
                        return
                    } else if possibleFreq > 1_000 {
                        frequency = possibleFreq / 1_000.0
                        return
                    } else {
                        frequency = possibleFreq
                        return
                    }
                }
            }
        }

        // Check children
        var children: io_iterator_t = 0
        if IORegistryEntryGetChildIterator(service, kIOServicePlane, &children) == KERN_SUCCESS {
            var child = IOIteratorNext(children)
            while child != 0 {
                searchRegistry(service: child, depth: depth + 1)
                IOObjectRelease(child)
                if frequency > 0 { break }
                child = IOIteratorNext(children)
            }
            IOObjectRelease(children)
        }
    }

    let rootService = IORegistryGetRootEntry(kIOMasterPortDefault)
    searchRegistry(service: rootService)
    IOObjectRelease(rootService)

    return frequency
}

private func getServiceProperties(_ service: io_registry_entry_t) -> [String: Any] {
    var propertiesDict: Unmanaged<CFMutableDictionary>?

    if IORegistryEntryCreateCFProperties(service, &propertiesDict, kCFAllocatorDefault, 0) != KERN_SUCCESS {
        return [:]
    }

    if let dict = propertiesDict?.takeRetainedValue() as? [String: Any] {
        return dict
    }

    return [:]
}