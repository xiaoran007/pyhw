FROM ubuntu:16.04 AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    wget

WORKDIR /build

COPY nvml.h /usr/include/

COPY nvmlGPULib.cpp .

RUN g++ -fPIC -shared -o nvmlGPULib.so nvmlGPULib.cpp -ldl

FROM scratch
COPY --from=builder /build/nvmlGPULib.so /