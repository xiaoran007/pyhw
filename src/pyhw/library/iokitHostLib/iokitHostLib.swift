import Foundation
import IOKit

@_cdecl("getHostInfo")
public func getHostInfo() -> UnsafePointer<CChar>? {
    let registryEntry = IOServiceGetMatchingService(kIOMasterPortDefault, IOServiceNameMatching("product"))
    guard registryEntry != 0 else {
//         print("Failed to get IOPlatformExpertDevice service")
        return UnsafePointer(strdup("Error"))
    }
    defer {
        IOObjectRelease(registryEntry)
    }

    var hostInfo = [String]()

    if let product = IORegistryEntryCreateCFProperty(registryEntry, "product-name" as CFString, kCFAllocatorDefault, 0)?.takeUnretainedValue() as? Data,
       let productName = String(data: product, encoding: .utf8) {
        hostInfo.append("\(productName)")
    } else {
        hostInfo.append("")
    }

    let resultString = hostInfo.joined(separator: "; ")
    let cString = strdup(resultString)

    return UnsafePointer(cString)
}