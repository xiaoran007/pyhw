from .nicInfo import NICInfo
import subprocess


class NICDetectMacOS:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__getNICInfo()
        return self.__nicInfo

    def __getNICInfo(self):
        try:
            # Get default interface
            cmd_get_interface = "route get default | grep interface"
            interface_output = subprocess.run(["bash", "-c", cmd_get_interface],
                                              capture_output=True, text=True).stdout.strip()
            interface = interface_output.split(":")[1].strip()

            # Get IP address
            if_ip = subprocess.run(["bash", "-c", f"ipconfig getifaddr {interface}"],
                                   capture_output=True, text=True).stdout.strip()

            # Get interface type and link speed
            link_info = self.__getLinkInfo(interface)

            # Add all information to nicInfo
            self.__nicInfo.nics.append(f"{interface} @ {if_ip} - {link_info}")
            self.__nicInfo.number += 1
        except Exception as e:
            self.__handleError()

    def __getLinkInfo(self, interface):
        try:
            # Check if interface is wireless
            is_wifi_cmd = f"networksetup -getairportpower {interface} 2>/dev/null"
            is_wifi_result = subprocess.run(["bash", "-c", is_wifi_cmd],
                                            capture_output=True, text=True).returncode

            if is_wifi_result == 0:  # This is a Wi-Fi interface
                speed, channel, band = self.__getWifiInfo(interface)
                return f"Wi-Fi {band} ({speed} Mbps)"
            else:
                # For wired connections, get link speed using networksetup
                media_cmd = f"networksetup -getmedia {interface} | grep 'Active'"
                media_info = subprocess.run(["bash", "-c", media_cmd],
                                            capture_output=True, text=True).stdout.strip()

                if media_info:
                    parts = media_info.split(':', 1)
                    if len(parts) > 1:
                        # Extract "2500Base-T <full-duplex>" part
                        media_details = parts[1].strip()

                        # Parse the speed part (e.g., "2500Base-T")
                        speed_part = media_details.split()[0] if media_details else ""

                        if "2500Base-T" in speed_part:
                            return "Wired (2.5 Gbps)"
                        elif "1000Base-T" in speed_part:
                            return "Wired (1 Gbps)"
                        elif "100Base-T" in speed_part:
                            return "Wired (100 Mbps)"
                        elif "10000Base-T" in speed_part:
                            return "Wired (10 Gbps)"
                        elif "Base-T" in speed_part or "base-T" in speed_part:
                            # Extract the numeric part from formats like "5000Base-T"
                            import re
                            speed_match = re.search(r'(\d+)(?:Base-T|base-T)', speed_part)
                            if speed_match:
                                speed_value = int(speed_match.group(1))
                                if speed_value >= 1000:
                                    return f"Wired ({speed_value / 1000:.1f} Gbps)"
                                else:
                                    return f"Wired ({speed_value} Mbps)"
                            return f"Wired ({speed_part})"
        except:
            return "Unknown connection type"

    def __getWifiInfo(self, interface):
        # 使用 system_profiler 获取 WiFi 信息
        profiler_cmd = f"system_profiler SPAirPortDataType -json"
        try:
            wifi_data = subprocess.run(["bash", "-c", profiler_cmd],
                                       capture_output=True, text=True, timeout=5).stdout

            import json
            data = json.loads(wifi_data)

            # 根据实际 JSON 结构提取信息
            if 'SPAirPortDataType' in data and isinstance(data['SPAirPortDataType'], list):
                airport_data = data['SPAirPortDataType'][0]

                # 获取接口列表
                if 'spairport_airport_interfaces' in airport_data:
                    interfaces = airport_data['spairport_airport_interfaces']

                    # 查找匹配的接口
                    for iface in interfaces:
                        if interface == iface.get('_name', ''):
                            # 获取当前网络信息
                            current_network = iface.get('spairport_current_network_information', {})

                            # 从当前连接中提取速率
                            speed = current_network.get('spairport_network_rate', 'Unknown')

                            # 获取信道信息
                            channel_info = current_network.get('spairport_network_channel', 'Unknown')

                            # 确定频段信息
                            band = "Unknown"
                            if isinstance(channel_info, str) and "GHz" in channel_info:
                                if "2GHz" in channel_info:
                                    band = "2.4GHz"
                                elif "5GHz" in channel_info:
                                    band = "5GHz"
                                elif "6GHz" in channel_info:
                                    band = "6GHz"

                            return speed, channel_info, band

            return "Unknown", "Unknown", "Unknown"
        except Exception as e:
            # 可以考虑添加日志记录 print(f"WiFi info error: {str(e)}")
            return "Unknown", "Unknown", "Unknown"

    def __handleError(self):
        self.__nicInfo.nics.append("en0 - Unknown connection")
        self.__nicInfo.number = 1
