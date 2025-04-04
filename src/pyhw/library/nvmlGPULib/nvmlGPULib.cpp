#include <dlfcn.h>
#include <iostream>
#include <string>
#include <nvml.h>

typedef nvmlReturn_t (*nvmlInit_t)(void);
typedef nvmlReturn_t (*nvmlShutdown_t)(void);
typedef nvmlReturn_t (*nvmlDeviceGetHandleByIndex_t)(unsigned int, nvmlDevice_t*);
typedef nvmlReturn_t (*nvmlDeviceGetNumGpuCores_t)(nvmlDevice_t, unsigned int*);

extern "C" {
    unsigned int GetGPUCoreCount() {
        void* handle = dlopen("libnvidia-ml.so.1", RTLD_LAZY);
        if (!handle) {
            std::cerr << "Could not load nvml library: " << dlerror() << std::endl;
            return 0;
        }

        nvmlInit_t nvmlInit = (nvmlInit_t)dlsym(handle, "nvmlInit");
        nvmlShutdown_t nvmlShutdown = (nvmlShutdown_t)dlsym(handle, "nvmlShutdown");
        nvmlDeviceGetHandleByIndex_t nvmlDeviceGetHandleByIndex = 
            (nvmlDeviceGetHandleByIndex_t)dlsym(handle, "nvmlDeviceGetHandleByIndex");
        nvmlDeviceGetNumGpuCores_t nvmlDeviceGetNumGpuCores = 
            (nvmlDeviceGetNumGpuCores_t)dlsym(handle, "nvmlDeviceGetNumGpuCores");

        if (!nvmlInit || !nvmlShutdown || !nvmlDeviceGetHandleByIndex || !nvmlDeviceGetNumGpuCores) {
            std::cerr << "Could not load nvml functions: " << dlerror() << std::endl;
            dlclose(handle);
            return 0;
        }

        nvmlReturn_t result;
        unsigned int cudaCores = 0;

        result = nvmlInit();
        if (result != NVML_SUCCESS) {
            dlclose(handle);
            return 0;
        }

        nvmlDevice_t device;
        result = nvmlDeviceGetHandleByIndex(0, &device);
        if (result != NVML_SUCCESS) {
            nvmlShutdown();
            dlclose(handle);
            return 0;
        }

        result = nvmlDeviceGetNumGpuCores(device, &cudaCores);
        if (result != NVML_SUCCESS) {
            nvmlShutdown();
            dlclose(handle);
            return 0;
        }

        nvmlShutdown();
        dlclose(handle);
        return cudaCores;
    }
}