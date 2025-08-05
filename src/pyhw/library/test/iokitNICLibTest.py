import ctypes
from ctypes import c_char_p, c_bool, c_int32, c_char, byref, create_string_buffer
import os


def main():
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建动态库路径（假设动态库在上级目录的lib文件夹中）
    lib_path = os.path.join(current_dir, "../lib/iokitNICLib.dylib")

    try:
        # 加载动态库
        lib = ctypes.CDLL(lib_path)

        # 设置函数参数和返回类型
        lib.getDefaultInterface.argtypes = [c_char_p]
        lib.getDefaultInterface.restype = c_bool

        lib.getNetworkInfo.argtypes = [c_char_p, ctypes.POINTER(c_bool),
                                       c_char_p, ctypes.POINTER(c_int32),
                                       c_char_p, c_char_p, c_char_p, c_char_p]
        lib.getNetworkInfo.restype = c_bool

        # 获取默认接口
        interface = create_string_buffer(32)
        if lib.getDefaultInterface(interface):
            interface_str = interface.value.decode('utf-8')
            print(f"默认网络接口: {interface_str}")

            # 获取网络信息
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

                # 输出获取到的信息
                print("=== 网络信息 ===")
                print(f"接口: {interface_str}")
                print(f"IP地址: {ip_address.value.decode('utf-8')}")
                print(f"连接类型: {conn_type.value.decode('utf-8')}")
                print(f"速度: {speed.value} Mbps")

                if is_wifi.value:
                    print(f"Wi-Fi频段: {band.value.decode('utf-8')}")
                    print(f"信道: {channel.value.decode('utf-8')}")
                    print(f"Wi-Fi标准: {wifi_standard.value.decode('utf-8')}")

                # 格式化输出（与nicInfo类似的格式）
                if is_wifi.value:
                    wifi_info = f"{wifi_standard.value.decode('utf-8')} {band.value.decode('utf-8')}"
                    conn_info = f"{conn_type.value.decode('utf-8')} ({wifi_info}, {speed.value} Mbps)"
                else:
                    conn_info = conn_type.value.decode('utf-8')

                formatted_output = f"{interface_str} @ {ip_address.value.decode('utf-8')} - {conn_info}"
                print("\n格式化输出:")
                print(formatted_output)
            else:
                print(f"无法获取接口 {interface_str} 的网络信息")
        else:
            print("无法获取默认网络接口")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()

