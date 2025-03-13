import ctypes


def main():
    lib = ctypes.CDLL(f"../lib/iokitHostLib.dylib")
    lib.getHostInfo.restype = ctypes.c_char_p
    host_info = lib.getHostInfo()
    print(host_info)
    # gpus = host_info.decode('utf-8').split("; ")


if __name__ == "__main__":
    main()
