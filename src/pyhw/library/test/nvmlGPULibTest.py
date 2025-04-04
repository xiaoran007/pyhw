import ctypes


def main():
    lib = ctypes.CDLL(f"../lib/nvmlGPULib_amd64.so")
    lib.GetGPUCoreCount.restype = ctypes.c_uint
    cuda_cores = lib.GetGPUCoreCount()
    print("CUDA Cores:", cuda_cores)


if __name__ == "__main__":
    main()
