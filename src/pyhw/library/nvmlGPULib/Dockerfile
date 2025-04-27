FROM xiaoran007/pyhw_builder:16.04 AS builder

WORKDIR /build

COPY nvml.h /usr/include/

COPY nvmlGPULib.cpp .

RUN g++ -fPIC -shared -o nvmlGPULib.so nvmlGPULib.cpp -ldl

FROM scratch
COPY --from=builder /build/nvmlGPULib.so /