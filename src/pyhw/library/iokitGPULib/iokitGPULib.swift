import Foundation
import IOKit


@_cdecl("getGPUInfo")
public func getGPUInfo() -> UnsafePointer<CChar>? {
    let matchingDict = IOServiceMatching("IOPCIDevice")
    var iterator: io_iterator_t = 0

    let result = IOServiceGetMatchingServices(kIOMasterPortDefault, matchingDict, &iterator)
    guard result == KERN_SUCCESS else {
        print("Failed to get matching services")
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
    
    // // Print detected GPUs
    // if gpuNames.isEmpty {
    //     print("No GPUs found.")
    // } else {
    //     print("Detected GPUs:")
    //     for gpu in gpuNames {
    //         print("  GPU: \(gpu)")
    //     }
    // }

    let cleanedGpuNames = gpuInfos.map { $0.replacingOccurrences(of: "\u{0000}", with: "") }

    let resultString = cleanedGpuNames.joined(separator: "; ")
    let cString = strdup(resultString)
    
    return UnsafePointer(cString)
}