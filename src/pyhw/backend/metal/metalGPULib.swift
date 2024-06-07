import Foundation
import Metal

@_cdecl("my_func")
public func my_func() -> UnsafePointer<CChar>? {
    var result: String;
    if let defaultDevice = MTLCreateSystemDefaultDevice() {
        result = defaultDevice.name
    }
    else {
        result = "None"
    }
    let cString = strdup(result)
    return UnsafePointer(cString)
}


@_cdecl("pr")
public func pr() -> CInt {
    return CInt(114514)
}
