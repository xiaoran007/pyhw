import ctypes


def main():
    lib = ctypes.CDLL(f"../lib/iokitCPULib.dylib")
    lib.get_apple_silicon_max_frequency.restype = ctypes.c_double
    max_freq = lib.get_apple_silicon_max_frequency()
    print(max_freq)
    # gpus = host_info.decode('utf-8').split("; ")


if __name__ == "__main__":
    main()


