CC = swiftc
CFLAG = -framework Metal -framework CoreGraphics

MACOS_VERSION = 10.15
ARCH_X86_64 = -target x86_64-apple-macos$(MACOS_VERSION)
ARCH_ARM64 = -target arm64-apple-macos$(MACOS_VERSION)

src = metalGPULib.swift

x86_64_lib: $(src)
	$(CC) -emit-library $(src) $(CFLAG) $(ARCH_X86_64) -o metalGPULib_x86_64.dylib

arm_lib: $(src)
	$(CC) -emit-library $(src) $(CFLAG) $(ARCH_ARM64) -o metalGPULib_arm64.dylib

lib: x86_64_lib arm_lib
	lipo -create metalGPULib_x86_64.dylib metalGPULib_arm64.dylib -output metalGPULib.dylib
	-rm metalGPULib_x86_64.dylib metalGPULib_arm64.dylib

x86_64_exe: metalGPU.swift
	$(CC) metalGPU.swift $(CFLAG) $(ARCH_X86_64) -o metalGPU_x86_64
arm_exe: metalGPU.swift
	$(CC) metalGPU.swift $(CFLAG) $(ARCH_ARM64) -o metalGPU_arm64
main: x86_64_exe arm_exe
	lipo -create metalGPU_x86_64 metalGPU_arm64 -output metalGPU
	-rm metalGPU_x86_64 metalGPU_arm64

.PHONY: clean
clean:
	-rm metalGPULib_x86_64.dylib metalGPULib_arm64.dylib metalGPU_x86_64 metalGPU_arm64 metalGPU