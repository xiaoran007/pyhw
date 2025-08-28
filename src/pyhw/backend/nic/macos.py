from .nicInfo import NICInfo
import subprocess
import ctypes
from ctypes import c_char_p, c_bool, c_int32, c_char, byref, create_string_buffer
from pathlib import Path


class NICDetectMacOS:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__getNICInfo()
        return self.__nicInfo

    def __getNICInfo(self):
        # Try to get NIC info using IOKit first
        if not self.__getNICInfoIOKit():
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
        else:
            pass

    def __getNICInfoIOKit(self):
        try:
            package_root = Path(__file__).resolve().parent.parent.parent
            lib = ctypes.CDLL(f"{package_root}/library/lib/iokitNICLib.dylib")

            lib.getDefaultInterface.argtypes = [c_char_p]
            lib.getDefaultInterface.restype = c_bool

            lib.getNetworkInfo.argtypes = [c_char_p, ctypes.POINTER(c_bool),
                                           c_char_p, ctypes.POINTER(c_int32),
                                           c_char_p, c_char_p, c_char_p, c_char_p]
            lib.getNetworkInfo.restype = c_bool
            interface = create_string_buffer(32)
            if lib.getDefaultInterface(interface):
                interface_str = interface.value.decode('utf-8')

                is_wifi = c_bool(False)
                ip_address = create_string_buffer(32)
                speed = c_int32(0)
                band = create_string_buffer(16)
                channel = create_string_buffer(32)
                conn_type = create_string_buffer(32)
                wifi_standard = create_string_buffer(16)

                if lib.getNetworkInfo(interface_str.encode('utf-8'),
                                      byref(is_wifi),
                                      ip_address,
                                      byref(speed),
                                      band,
                                      channel,
                                      conn_type,
                                      wifi_standard):

                    if is_wifi.value:
                        conn_info = f"{conn_type.value.decode('utf-8')} ({wifi_standard.value.decode('utf-8')} {band.value.decode('utf-8')} {speed.value} Mbps)"
                    else:
                        conn_info = conn_type.value.decode('utf-8')

                    formatted_output = f"{interface_str} @ {ip_address.value.decode('utf-8')} - {conn_info}"

                    self.__nicInfo.nics.append(formatted_output)
                    self.__nicInfo.number += 1

                    return True

                else:
                    return False
            else:
                return False

        except Exception as e:
            # print(f"An error occurred while getting NIC info using IOKit: {e}")
            return False

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
        # Use system_profiler to get WiFi information
        profiler_cmd = f"system_profiler SPAirPortDataType -json"
        try:
            wifi_data = subprocess.run(["bash", "-c", profiler_cmd],
                                       capture_output=True, text=True, timeout=5).stdout

            import json
            data = json.loads(wifi_data)

            # Extract information based on the JSON structure
            if 'SPAirPortDataType' in data and isinstance(data['SPAirPortDataType'], list):
                airport_data = data['SPAirPortDataType'][0]

                # Get the interface list
                if 'spairport_airport_interfaces' in airport_data:
                    interfaces = airport_data['spairport_airport_interfaces']

                    # Find the matching interface
                    for iface in interfaces:
                        if interface == iface.get('_name', ''):
                            # Get current network information
                            current_network = iface.get('spairport_current_network_information', {})

                            # Extract speed rate from current connection
                            speed = current_network.get('spairport_network_rate', 'Unknown')

                            # Get channel information
                            channel_info = current_network.get('spairport_network_channel', 'Unknown')

                            # Determine frequency band information
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
            # Consider adding logging here: print(f"WiFi info error: {str(e)}")
            return "Unknown", "Unknown", "Unknown"

    def __handleError(self):
        self.__nicInfo.nics.append("en0 - Unknown connection")
        self.__nicInfo.number = 1
