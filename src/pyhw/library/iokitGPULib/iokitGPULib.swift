import Foundation
import IOKit


@_cdecl("getGPUInfo")
public func getGPUInfo() -> UnsafePointer<CChar>? {
    let matchingDict = IOServiceMatching("IOPCIDevice")
    var iterator: io_iterator_t = 0

    let result = IOServiceGetMatchingServices(kIOMasterPortDefault, matchingDict, &iterator)
    guard result == KERN_SUCCESS else {
        return UnsafePointer(strdup("Error"))
    }
    
    var gpuInfos = [String]()
    
    var service = IOIteratorNext(iterator)
    while service != 0 {
        var properties: Unmanaged<CFMutableDictionary>?
        if IORegistryEntryCreateCFProperties(service, &properties, kCFAllocatorDefault, 0) == KERN_SUCCESS,
           let props = properties?.takeRetainedValue() as? [String: Any] {
            
            if let modelData = props["model"] as? Data,
               let modelName = String(data: modelData, encoding: .utf8) {
                let vendorID = (props["vendor-id"] as? Data).flatMap { $0.withUnsafeBytes { $0.load(as: UInt32.self) } } ?? 0
                let memorySizeMB = props["VRAM,totalMB"] ?? 0
                let gpuInfo = "\(modelName), \(String(format: "0x%04X", vendorID)), \(memorySizeMB)"
                gpuInfos.append(gpuInfo)
            }
        }
        
        IOObjectRelease(service)
        service = IOIteratorNext(iterator)
    }
    
    IOObjectRelease(iterator)


    let cleanedGpuNames = gpuInfos.map { $0.replacingOccurrences(of: "\u{0000}", with: "") }

    let resultString = cleanedGpuNames.joined(separator: "; ")
    let cString = strdup(resultString)
    
    return UnsafePointer(cString)
}


@_cdecl("getAppleSiliconGPUInfo")
public func getAppleSiliconGPUInfo() -> UnsafePointer<CChar>? {
    let matchingDict = IOServiceMatching("AGXAccelerator")
    var iterator: io_iterator_t = 0

    guard IOServiceGetMatchingServices(kIOMasterPortDefault, matchingDict, &iterator) == KERN_SUCCESS else {
        return UnsafePointer(strdup("0"))
    }

    var gpuCores = 0

    let service = IOIteratorNext(iterator)
    if service != 0 {
        var properties: Unmanaged<CFMutableDictionary>?
        if IORegistryEntryCreateCFProperties(service, &properties, kCFAllocatorDefault, 0) == KERN_SUCCESS,
           let props = properties?.takeRetainedValue() as? [String: Any],
           let cores = props["gpu-core-count"] as? Int {
            gpuCores = cores
        }
        IOObjectRelease(service)
    }

    IOObjectRelease(iterator)

    return UnsafePointer(strdup(String(gpuCores)))
}