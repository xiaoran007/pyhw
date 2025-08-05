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
                         connectionType: UnsafeMutablePointer<Int8>,
                         wifiStandard: UnsafeMutablePointer<Int8>) -> Bool {

    let interfaceNameStr = String(cString: interfaceName)

    isWifi.pointee = false

    if let ip = getIPAddress(for: interfaceNameStr) {
        strncpy(ipAddress, ip, 16)
    } else {
        strncpy(ipAddress, "Unknown", 16)
    }

    if let wifiInterface = CWWiFiClient.shared().interface(withName: interfaceNameStr) {
        isWifi.pointee = true

        if let wifiInfo = getWifiInfo(interface: wifiInterface) {
            speed.pointee = Int32(wifiInfo.speed)
            strncpy(band, wifiInfo.band, 10)
            strncpy(channel, wifiInfo.channel, 20)
            strncpy(connectionType, "Wi-Fi", 20)
            strncpy(wifiStandard, wifiInfo.standard, 10)
        } else {
            speed.pointee = 0
            strncpy(band, "Unknown", 10)
            strncpy(channel, "Unknown", 20)
            strncpy(connectionType, "Wi-Fi", 20)
            strncpy(wifiStandard, "Unknown", 10)
        }

        return true
    } else {
        if let wiredSpeed = getWiredSpeed(for: interfaceNameStr) {
            speed.pointee = Int32(wiredSpeed)

            if  wiredSpeed >= 40000 {
                strncpy(connectionType, "Wired (40 Gbps)", 20)
            } else if wiredSpeed >= 25000 {
                strncpy(connectionType, "Wired (25 Gbps)", 20)
            } else if wiredSpeed >= 10000 {
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
            strncpy(wifiStandard, "N/A", 10)

            return true
        }
    }

    speed.pointee = 0
    strncpy(band, "Unknown", 10)
    strncpy(channel, "Unknown", 20)
    strncpy(connectionType, "Unknown", 20)
    strncpy(wifiStandard, "Unknown", 10)

    return true
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
        if addrFamily == UInt8(AF_INET) {
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
    var standard: String
}

func getWifiInfo(interface: CWInterface) -> WiFiInfo? {
    guard interface.powerOn() else { return nil }

    let speed = Int(interface.transmitRate())
    var band = "Unknown"
    var channel = "Unknown"
    var standard = "Unknown"

    standard = determineWiFiStandard(interface: interface)

    if let channelInfo = interface.wlanChannel() {
        channel = "\(channelInfo.channelNumber)"

        if channelInfo.channelBand == .band2GHz {
            band = "2.4 GHz"
        } else if channelInfo.channelBand == .band5GHz {
            band = "5 GHz"
        } else if #available(macOS 13.0, *), channelInfo.channelBand == .band6GHz {
            band = "6 GHz"
        }
    }

    return WiFiInfo(speed: speed, band: band, channel: channel, standard: standard)
}

func determineWiFiStandard(interface: CWInterface) -> String {
    if #available(macOS 10.15, *) {
        let phyMode = interface.activePHYMode()

        switch phyMode {
        case .mode11ax:
            return "ax"
        case .mode11ac:
            return "ac"
        case .mode11n:
            return "n"
        case .mode11a:
            return "a"
        case .mode11b:
            return "b"
        case .mode11g:
            return "g"
        default:
            break
        }
    }

    return ""
}

func getWiredSpeed(for interface: String) -> Int? {
    var speed: Int? = nil

    let task = Process()
    task.launchPath = "/usr/sbin/networksetup"
    task.arguments = ["-getmedia", interface]

    let pipe = Pipe()
    task.standardOutput = pipe

    do {
        try task.run()
        task.waitUntilExit()
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        let output = String(data: data, encoding: .utf8) ?? ""

        if output.contains("40000Base-T") {
            speed = 40000
        } else if output.contains("25000Base-T") {
            speed = 25000
        } else if output.contains("10000Base-T") {
            speed = 10000
        } else if output.contains("5000Base-T") {
            speed = 5000
        } else if output.contains("2500Base-T") {
            speed = 2500
        } else if output.contains("1000Base-T") {
            speed = 1000
        } else if output.contains("100Base-T") {
            speed = 100
        } else if output.contains("10Base-T") {
            speed = 10
        }
    } catch {
        speed = 0
    }

    if speed == nil {
        let matchingDict = IOServiceMatching("IONetworkInterface") as NSMutableDictionary

        var iterator: io_iterator_t = 0
        if IOServiceGetMatchingServices(kIOMasterPortDefault, matchingDict, &iterator) == KERN_SUCCESS {
            defer { IOObjectRelease(iterator) }

            var service: io_object_t = 0
            repeat {
                service = IOIteratorNext(iterator)
                guard service != 0 else { break }
                defer { IOObjectRelease(service) }

                if let bsdNameRef = IORegistryEntryCreateCFProperty(service, "BSD Name" as CFString, kCFAllocatorDefault, 0),
                   let ifName = (bsdNameRef.takeRetainedValue() as? String),
                   ifName == interface {

                    var parentService: io_object_t = 0
                    if IORegistryEntryGetParentEntry(service, kIOServicePlane, &parentService) == KERN_SUCCESS {
                        defer { IOObjectRelease(parentService) }

                        let keysToCheck = ["IOLinkSpeed", "LinkSpeed", "CurrentLinkSpeed"]

                        for key in keysToCheck {
                            if let speedRef = IORegistryEntryCreateCFProperty(parentService, key as CFString, kCFAllocatorDefault, 0),
                               let linkSpeed = speedRef.takeRetainedValue() as? Int {
                                speed = linkSpeed >= 1000000 ? linkSpeed / 1000000 : linkSpeed
                                break
                            }
                        }

                        if speed == nil {
                            let mediaProps = ["IOMediaAdditions", "Media", "LinkStatus"]
                            for prop in mediaProps {
                                if let mediaRef = IORegistryEntryCreateCFProperty(parentService, prop as CFString, kCFAllocatorDefault, 0) {
                                    if let mediaDict = mediaRef.takeRetainedValue() as? [String: Any] {
                                        if let activeInfo = mediaDict["Active"] as? [String: Any],
                                           let speedStr = activeInfo["String"] as? String {
                                            if speedStr.contains("10000") {
                                                speed = 10000
                                            } else if speedStr.contains("5000") {
                                                speed = 5000
                                            } else if speedStr.contains("2500") {
                                                speed = 2500
                                            } else if speedStr.contains("1000") {
                                                speed = 1000
                                            } else if speedStr.contains("100") {
                                                speed = 100
                                            } else if speedStr.contains("10") {
                                                speed = 10
                                            }
                                            break
                                        }
                                    }
                                }
                            }
                        }
                    }

                    break
                }
            } while service != 0
        }
    }

    return speed
}

@_cdecl("getDefaultInterface")
public func getDefaultInterface(_ interfaceName: UnsafeMutablePointer<Int8>) -> Bool {
    var defaultRouteInterface: String?

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
        defaultRouteInterface = "en0"
    }

    strncpy(interfaceName, defaultRouteInterface!, 16)

    return true
}