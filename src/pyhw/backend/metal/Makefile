CC = swiftc
CFLAG = -framework Metal -framework CoreGraphics

MACOS_VERSION = 10.15
ARCH_X86_64 = -target x86_64-apple-macos$(MACOS_VERSION)
ARCH_ARM64 = -target arm64-apple-macos$(MACOS_VERSION)


x86_64: metalGPU.swift
	$(CC) metalGPU.swift $(CFLAG) $(ARCH_X86_64) -o metalGPU_x86_64
arm: metalGPU.swift
	$(CC) metalGPU.swift $(CFLAG) $(ARCH_ARM64) -o metalGPU_arm64
main: x86_64 arm
	lipo -create metalGPU_x86_64 metalGPU_arm64 -output metalGPU
	-rm metalGPU_x86_64 metalGPU_arm64