import ctypes


def main():
    lib = ctypes.CDLL(f"../lib/iokitCPULib.dylib")
    lib.getPCoreFrequency.restype = ctypes.c_double
    host_info = lib.getPCoreFrequency()
    print(host_info)
    lib.getECoreFrequency.restype = ctypes.c_double
    host_info = lib.getECoreFrequency()
    print(host_info)
    # gpus = host_info.decode('utf-8').split("; ")


if __name__ == "__main__":
    main()


