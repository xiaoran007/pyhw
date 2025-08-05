import ctypes


def main():
    lib = ctypes.CDLL(f"../lib/iokitGPULib.dylib")
    lib.getGPUInfo.restype = ctypes.c_char_p
    lib.getAppleSiliconGPUInfo.restype = ctypes.c_char_p
    gpu_info = lib.getAppleSiliconGPUInfo()
    print(gpu_info.decode('utf-8'))


if __name__ == "__main__":
    main()




