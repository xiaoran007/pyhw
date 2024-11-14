import Foundation
import IOKit


@_cdecl("getHostInfo")
public func getHostInfo() -> UnsafePointer<CChar>? {
    let registryEntry = IOServiceGetMatchingService(kIOMasterPortDefault, IOServiceMatching("product"))
    guard registryEntry != 0 else {
        print("Failed to get product service")
        return UnsafePointer(strdup("Error"))
    }
    defer {
        IOObjectRelease(registryEntry)
    }

    var hostInfo = [String]()

    if let product = IORegistryEntryCreateCFProperty(registryEntry, "product-name" as CFString, kCFAllocatorDefault, 0)?.takeUnretainedValue() as? String {
        hostInfo.append("\(product)")
    } else {
        hostInfo.append("")
    }

    let resultString = hostInfo.joined(separator: "; ")
    let cString = strdup(resultString)
    
    return UnsafePointer(cString)
}