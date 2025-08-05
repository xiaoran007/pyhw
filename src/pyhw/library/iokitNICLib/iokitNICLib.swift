import Foundation
import CoreWLAN
import Network
import SystemConfiguration
import IOKit
import IOKit.network

@_cdecl("getNetworkInfo")
public func getNetworkInfo(_ interfaceName: UnsafePointer<Int8>,
                         isWifi: UnsafeMutablePointer<Bool>,
                         ipAddress: UnsafeMutablePointer<Int8>,
                         speed: UnsafeMutablePointer<Int32>,
                         band: UnsafeMutablePointer<Int8>,
                         channel: UnsafeMutablePointer<Int8>,
                         connectionType: UnsafeMutablePointer<Int8>) -> Bool {

    let interfaceNameStr = String(cString: interfaceName)

    // 默认设置isWifi为false
    isWifi.pointee = false

    // 获取IP地址
    if let ip = getIPAddress(for: interfaceNameStr) {
        strncpy(ipAddress, ip, 16)
    } else {
        strncpy(ipAddress, "Unknown", 16)
    }

    // 检查是否为WiFi接口
    if let wifiInterface = CWWiFiClient.shared().interface(withName: interfaceNameStr) {
        isWifi.pointee = true

        // 获取WiFi信息
        if let wifiInfo = getWifiInfo(interface: wifiInterface) {
            speed.pointee = Int32(wifiInfo.speed)
            strncpy(band, wifiInfo.band, 10)
            strncpy(channel, wifiInfo.channel, 20)
            strncpy(connectionType, "Wi-Fi", 20)
        } else {
            speed.pointee = 0
            strncpy(band, "Unknown", 10)
            strncpy(channel, "Unknown", 20)
            strncpy(connectionType, "Wi-Fi", 20)
        }

        return true
    } else {
        // 有线网络信息获取
        if let wiredSpeed = getWiredSpeed(for: interfaceNameStr) {
            speed.pointee = Int32(wiredSpeed)

            // 设置连接类型
            if wiredSpeed >= 10000 {
                strncpy(connectionType, "Wired (10 Gbps)", 20)
            } else if wiredSpeed >= 5000 {
                strncpy(connectionType, "Wired (5 Gbps)", 20)
            } else if wiredSpeed >= 2500 {
                strncpy(connectionType, "Wired (2.5 Gbps)", 20)
            } else if wiredSpeed >= 1000 {
                strncpy(connectionType, "Wired (1 Gbps)", 20)
            } else if wiredSpeed >= 100 {
                strncpy(connectionType, "Wired (100 Mbps)", 20)
            } else {
                strncpy(connectionType, "Wired", 20)
            }

            strncpy(band, "N/A", 10)
            strncpy(channel, "N/A", 20)

            return true
        }
    }

    // 如果没有获取到有效信息
    speed.pointee = 0
    strncpy(band, "Unknown", 10)
    strncpy(channel, "Unknown", 20)
    strncpy(connectionType, "Unknown", 20)

    return false
}

func getIPAddress(for interface_name: String) -> String? {
    var address: String?
    var ifaddr: UnsafeMutablePointer<ifaddrs>?

    guard getifaddrs(&ifaddr) == 0 else { return nil }
    defer { freeifaddrs(ifaddr) }

    var ptr = ifaddr
    while ptr != nil {
        defer { ptr = ptr?.pointee.ifa_next }

        let interface = ptr?.pointee
        let addrFamily = interface?.ifa_addr.pointee.sa_family
        if addrFamily == UInt8(AF_INET) {  // 只获取IPv4地址
            let name = String(cString: (interface?.ifa_name)!)
            if name == interface_name {
                var hostname = [CChar](repeating: 0, count: Int(NI_MAXHOST))
                getnameinfo(interface?.ifa_addr, socklen_t((interface?.ifa_addr.pointee.sa_len)!),
                           &hostname, socklen_t(hostname.count),
                           nil, 0, NI_NUMERICHOST)
                address = String(cString: hostname)
            }
        }
    }

    return address
}

struct WiFiInfo {
    var speed: Int
    var band: String
    var channel: String
}

func getWifiInfo(interface: CWInterface) -> WiFiInfo? {
    guard interface.powerOn() else { return nil }

    let speed = Int(interface.transmitRate())
    var band = "Unknown"
    var channel = "Unknown"

    if let channelInfo = interface.wlanChannel() {
        channel = "\(channelInfo.channelNumber)"

        // 确定频段
        if channelInfo.channelBand == .band2GHz {
            band = "2.4GHz"
        } else if channelInfo.channelBand == .band5GHz {
            band = "5GHz"
        } else if #available(macOS 13.0, *), channelInfo.channelBand == .band6GHz {
            band = "6GHz"
        }
    }

    return WiFiInfo(speed: speed, band: band, channel: channel)
}

func getWiredSpeed(for interface: String) -> Int? {
    // 使用IOKit获取有线接口速度
    let matchingDict = IOServiceMatching("IONetworkInterface") as NSMutableDictionary

    var iterator: io_iterator_t = 0
    if IOServiceGetMatchingServices(kIOMasterPortDefault, matchingDict, &iterator) != KERN_SUCCESS {
        return nil
    }
    defer { IOObjectRelease(iterator) }

    var service: io_object_t = 0
    var speed: Int? = nil

    repeat {
        service = IOIteratorNext(iterator)
        guard service != 0 else { break }
        defer { IOObjectRelease(service) }

        var parentService: io_object_t = 0
        if IORegistryEntryGetParentEntry(service, kIOServicePlane, &parentService) == KERN_SUCCESS {
            defer { IOObjectRelease(parentService) }

            // 获取接口名称
            let interfaceNameRef = IORegistryEntryCreateCFProperty(service, "BSD Name" as CFString, kCFAllocatorDefault, 0)
            if let interfaceNameRef = interfaceNameRef,
               let ifName = (interfaceNameRef.takeRetainedValue() as? String),
               ifName == interface {

                // 检查接口是否为有线接口
                let interfaceTypeRef = IORegistryEntryCreateCFProperty(parentService, "IOInterfaceType" as CFString, kCFAllocatorDefault, 0)
                if let interfaceTypeRef = interfaceTypeRef,
                   let interfaceType = interfaceTypeRef.takeRetainedValue() as? Int,
                   interfaceType == 6 { // 6是有线以太网接口

                    // 获取链接速度
                    let linkStatusRef = IORegistryEntryCreateCFProperty(parentService, "IOLinkSpeed" as CFString, kCFAllocatorDefault, 0)
                    if let linkStatusRef = linkStatusRef,
                       let linkSpeed = linkStatusRef.takeRetainedValue() as? Int {
                        // IOLinkSpeed是以bps为单位，需要转换为Mbps
                        speed = linkSpeed / 1_000_000
                    }

                    // 如果无法通过IOLinkSpeed获取，尝试其他属性
                    if speed == nil || speed == 0 {
                        // 尝试获取媒体类型
                        let mediaDict = IORegistryEntryCreateCFProperty(parentService, "IOMediaAdditions" as CFString, kCFAllocatorDefault, 0)
                        if let mediaDict = mediaDict,
                           let mediaDictValue = mediaDict.takeRetainedValue() as? [String: Any],
                           let activeSubkey = mediaDictValue["Active"] as? [String: Any] {
                            // 通常包含如"1000baseT"的信息
                            if let speedStr = activeSubkey["String"] as? String {
                                if speedStr.contains("10000base") {
                                    speed = 10000
                                } else if speedStr.contains("5000base") {
                                    speed = 5000
                                } else if speedStr.contains("2500base") {
                                    speed = 2500
                                } else if speedStr.contains("1000base") {
                                    speed = 1000
                                } else if speedStr.contains("100base") {
                                    speed = 100
                                } else if speedStr.contains("10base") {
                                    speed = 10
                                }
                            }
                        }
                    }

                    break
                }
            }
        }
    } while service != 0

    // 如果找不到速度，使用备用方法
    if speed == nil {
        // 使用命令行工具作为备选
        let task = Process()
        task.launchPath = "/usr/sbin/networksetup"
        task.arguments = ["-getmedia", interface]

        let pipe = Pipe()
        task.standardOutput = pipe

        do {
            try task.run()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            let output = String(data: data, encoding: .utf8) ?? ""

            if output.contains("2500baseT") {
                speed = 2500
            } else if output.contains("1000baseT") {
                speed = 1000
            } else if output.contains("100baseT") {
                speed = 100
            } else if output.contains("10000baseT") {
                speed = 10000
            } else if output.contains("5000baseT") {
                speed = 5000
            }
        } catch {
            print("备用方法错误: \(error)")
        }
    }

    return speed
}

@_cdecl("getDefaultInterface")
public func getDefaultInterface(_ interfaceName: UnsafeMutablePointer<Int8>) -> Bool {
    var defaultRouteInterface: String?

    // 优先使用命令行方法获取默认路由接口
    let task = Process()
    task.launchPath = "/bin/bash"
    task.arguments = ["-c", "route -n get default 2>/dev/null | grep 'interface:' | awk '{print $2}'"]

    let pipe = Pipe()
    task.standardOutput = pipe

    do {
        try task.run()
        task.waitUntilExit()
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        if let output = String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines),
           !output.isEmpty {
            defaultRouteInterface = output
        }
    } catch {
        print("获取默认路由接口错误: \(error)")
    }

    // 如果还是找不到，使用en0作为备选
    defaultRouteInterface = defaultRouteInterface ?? "en0"

    // 复制接口名称到输出参数
    strncpy(interfaceName, defaultRouteInterface!, 16)

    return true
}