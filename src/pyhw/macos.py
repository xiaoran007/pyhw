import subprocess
import json
import platform
from pyhwException import GPUNotFoundException, BackendException


class GPUInfo:
    def __init__(self, verbose=False):
        self._gpus = list()
        self._verbose = verbose

    def init(self):
        pass

    def _get_gpu_info(self):
        try:
            gpus = json.loads(subprocess.check_output(["system_profiler", "SPDisplaysDataType", "-json"])).get('SPDisplaysDataType')
            if gpus is not None:
                if self._verbose:
                    print(f"Detected {len(gpus)} GPU(s).")
            else:
                raise GPUNotFoundException("No GPU information found.")
        except Exception as e:
            raise BackendException(f"An error occurred while getting GPU info: {e}")

        gpu_info_list = list()

        for i in range(len(gpus)):
            gpu = gpus[i]
            info = dict()
            info["name"] = gpu.get("sppci_model")
            if gpu.get("spdisplays_vendor") == "sppci_vendor_Apple":
                info["vram"] = f"{get_mem_info()} (shared memory)"
            else:
                info["vram"] = gpu.get("spdisplays_vram")
            info["vendor"] = gpu.get("spdisplays_vendor")
            info["cores"] = gpu.get("sppci_cores")
            info["metal"] = gpu.get("spdisplays_mtlgpufamilysupport")
            info["bus"] = gpu.get("sppci_bus")
            info["link"] = gpu.get("spdisplays_pcie_width")
            gpu_info_list.append(info)

    @staticmethod
    def _handleVendor(vendor):
        if vendor == "sppci_vendor_Apple":
            return "Apple"
        elif vendor == "sppci_vendor_intel":
            return "Intel"
        elif vendor == "sppci_vendor_amd":
            return "AMD"
        else:
            return vendor

    @staticmethod
    def _handleVram(vram, vendor):
        if vendor == "Apple":
            return f"{get_mem_info()} (shared memory)"
        else:
            return vram

    @staticmethod
    def _getVramApple():
        try:
            return json.loads(subprocess.check_output(["system_profiler", "SPHardwareDataType", "-json"]))["SPHardwareDataType"][0]["physical_memory"]
        except Exception as e:
            raise BackendException(f"An error occurred while getting memory info: {e}")


class GPU:
    def __init__(self):
        self._name = str()
        self._vram = str()
        self._vendor = str()
        self._cores = str()
        self._metal = str()
        self._bus = str()
        self._bus_width = str()
        self._id = int()

    def init(self):
        pass

    def _get_gpu_info(self):
        pass




def get_mem_info():
    try:
        mem_info_dict = json.loads(subprocess.check_output(["system_profiler", "SPHardwareDataType", "-json"]))
        mem_info = mem_info_dict["SPHardwareDataType"][0]["physical_memory"]
        return mem_info
    except Exception as e:
        print(f"An error occurred while getting memory info: {e}")
        exit(-1)


def get_gpu_info():
    gpus = list()
    try:
        gpu_info_dict = json.loads(subprocess.check_output(["system_profiler", "SPDisplaysDataType", "-json"]))
        if 'SPDisplaysDataType' in gpu_info_dict:
            gpus = gpu_info_dict['SPDisplaysDataType']
            print(f"Detected {len(gpus)} GPU(s).")
        else:
            print("No GPU information found.")
    except Exception as e:
        print(f"An error occurred while getting GPU info: {e}")
        exit(-1)

    gpu_info_list = list()

    for i in range(len(gpus)):
        gpu = gpus[i]
        info = dict()
        info["name"] = gpu.get("sppci_model")
        if gpu.get("spdisplays_vendor") == "sppci_vendor_Apple":
            info["vram"] = f"{get_mem_info()} (shared memory)"
        else:
            info["vram"] = gpu.get("spdisplays_vram")
        info["vendor"] = gpu.get("spdisplays_vendor")
        info["cores"] = gpu.get("sppci_cores")
        info["metal"] = gpu.get("spdisplays_mtlgpufamilysupport")
        info["bus"] = gpu.get("sppci_bus")
        info["link"] = gpu.get("spdisplays_pcie_width")
        gpu_info_list.append(info)
    return gpu_info_list


if __name__ == "__main__":
    li = get_gpu_info()
    for i in range(len(li)):
        info = li[i]
        print('----------')
        print(f"GPU {i}:")
        print(f'name: {info["name"]}')
        print(f'vram: {info["vram"]}')
        print(f'vendor: {info["vendor"]}')
        print(f'cores: {info["cores"]}')
        print(f'metal: {info["metal"]}')
        print(f'bus: {info["bus"]}')
        print(f'link: {info["link"]}')

        print('----------')

