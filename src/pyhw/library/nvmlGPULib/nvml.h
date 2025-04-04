#ifndef NVML_H
#define NVML_H

#ifdef __cplusplus
extern "C" {
#endif

#define NVML_DEVICE_NAME_BUFFER_SIZE                  64

typedef enum nvmlReturn_enum {
    NVML_SUCCESS = 0,
    NVML_ERROR_UNKNOWN = 999
} nvmlReturn_t;

typedef struct nvmlDevice_st* nvmlDevice_t;

const char* nvmlErrorString(nvmlReturn_t result);

nvmlReturn_t nvmlInit(void);
nvmlReturn_t nvmlShutdown(void);
nvmlReturn_t nvmlDeviceGetCount(unsigned int* deviceCount);
nvmlReturn_t nvmlDeviceGetHandleByIndex(unsigned int index, nvmlDevice_t* device);
nvmlReturn_t nvmlDeviceGetHandleByPciBusId_v2 (const char* pciBusId, nvmlDevice_t* device);
nvmlReturn_t nvmlDeviceGetName(nvmlDevice_t device, char* name, unsigned int length);
nvmlReturn_t nvmlDeviceGetUtilizationRates(nvmlDevice_t device, void* utilization);
nvmlReturn_t nvmlDeviceGetNumGpuCores(nvmlDevice_t device, unsigned int* numCores);

#ifdef __cplusplus
}
#endif

#endif