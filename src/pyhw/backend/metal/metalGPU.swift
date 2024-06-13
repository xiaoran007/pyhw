import Foundation
import Metal


// Function to list usable Metal GPUs
func listMetalGPUs() -> [String] {
    var gpuList: [String] = []

    // Get the default Metal device
    if let defaultDevice = MTLCreateSystemDefaultDevice() {
        printDeviceInfo(device: defaultDevice)
        gpuList.append(defaultDevice.name)
    }

    // Get all Metal devices
    let allDevices = MTLCopyAllDevices()
    print(allDevices)
    for device in allDevices {
        printDeviceInfo(device: device)
        gpuList.append(device.name)
    }

    return gpuList
}

// need compile flag -framework CoreGraphics
func printDeviceInfo(device: MTLDevice) {
    print("Device Name: \(device.name)")
    print("Max Threads Per Threadgroup: \(device.maxThreadsPerThreadgroup)")
    // print("Supports Feature Set macOS_GPUFamily1_v1: \(device.supportsFeatureSet(.macOS_GPUFamily1_v1))")
    // print("Supports Feature Set macOS_GPUFamily1_v2: \(device.supportsFeatureSet(.macOS_GPUFamily1_v2))")
    // print("Supports Feature Set macOS_GPUFamily1_v3: \(device.supportsFeatureSet(.macOS_GPUFamily1_v3))")
    // print("Supports Feature Set macOS_GPUFamily1_v4: \(device.supportsFeatureSet(.macOS_GPUFamily1_v4))")
    // print("Supports Feature Set macOS_GPUFamily2_v1: \(device.supportsFeatureSet(.macOS_GPUFamily2_v1))")
    // print("Supports Feature Set macOS_GPUFamily2_v2: \(device.supportsFeatureSet(.macOS_GPUFamily2_v2))")
    print("Supports Unified Memory: \(device.hasUnifiedMemory)")
    print("Registry ID: \(device.registryID)")
    print("CurrentAllocatedSize: \(device.currentAllocatedSize) bytes")
}

// Print the list of usable Metal GPUs
// let gpuList = listMetalGPUs()
// print("Usable Metal GPUs:")
// for gpu in gpuList {
//     print(gpu)
// }


// var device: MTLDevice!
// device = MTLCreateSystemDefaultDevice()
// printDeviceInfo(device: device)
if let defaultDevice = MTLCreateSystemDefaultDevice() {
    print("Default Metal Device Information:")
    printDeviceInfo(device: defaultDevice)
} else {
    print("No Metal-compatible device found.")
}



