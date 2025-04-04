import ctypes
import pypci


def main():
    lib = ctypes.CDLL(f"../lib/nvmlGPULib_amd64.so")
    lib.GetGPUCoreCount.argtypes = [ctypes.c_uint]
    lib.GetGPUCoreCount.restype = ctypes.c_uint
    cuda_cores = lib.GetGPUCoreCount(0)
    print("CUDA Cores:", cuda_cores)
    lib.GetGPUCoreCountByPciBusId.argtypes = [ctypes.c_char_p]
    lib.GetGPUCoreCountByPciBusId.restype = ctypes.c_uint
    pci_bus_id = b"00000000:99:00.0"
    cuda_cores = lib.GetGPUCoreCountByPciBusId(pci_bus_id)
    print("CUDA Cores by PCI Bus ID:", cuda_cores)

    gpu_devices = pypci.PCI().FindAllVGA()
    for gpu in gpu_devices:
        print(f"id: {gpu.bus}")
        print(f"cuda cores: {lib.GetGPUCoreCountByPciBusId(f'00000000:{gpu.bus}'.encode())}")
        


if __name__ == "__main__":
    main()
