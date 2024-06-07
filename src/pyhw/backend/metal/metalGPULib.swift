import Foundation
import Metal

struct MetalDevice {
    static var defaultDevice: MTLDevice?
}

@_cdecl("backend_init")
public func backend_init() {
    MetalDevice.defaultDevice = MTLCreateSystemDefaultDevice()
}

@_cdecl("get_default_device_name")
public func get_default_device_name() -> UnsafePointer<CChar>? {
    var result: String;
    if let defaultDevice = MetalDevice.defaultDevice {
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


