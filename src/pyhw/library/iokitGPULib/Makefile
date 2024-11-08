CC = swiftc
CFLAG = -framework IOKit

MACOS_VERSION = 11
ARCH_X86_64 = -target x86_64-apple-macos$(MACOS_VERSION)
ARCH_ARM64 = -target arm64-apple-macos$(MACOS_VERSION)

target = iokitGPULib
src = $(target).swift

x86_64_lib: $(src)
	$(CC) -emit-library $(src) $(CFLAG) $(ARCH_X86_64) -o $(target)_x86_64.dylib

arm_lib: $(src)
	$(CC) -emit-library $(src) $(CFLAG) $(ARCH_ARM64) -o $(target)_arm64.dylib

lib: x86_64_lib arm_lib
	-mkdir -p ../lib
	lipo -create $(target)_x86_64.dylib $(target)_arm64.dylib -output ../lib/$(target).dylib
	-rm $(target)_x86_64.dylib $(target)_arm64.dylib


.PHONY: clean
clean:
	-rm $(target)_x86_64.dylib $(target)_arm64.dylib $(target).dylib