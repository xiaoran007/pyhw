CC = clang
CFLAG = -framework IOKit -framework CoreFoundation

target = iokitCPULib
src = $(target).c

arm_lib: $(src)
	$(CC) -shared -fPIC $(src) -o $(target)_arm64.dylib $(CFLAG)

lib: arm_lib
	-mkdir -p ../lib
	-cp $(target)_arm64.dylib ../lib/$(target).dylib
	-rm $(target)_arm64.dylib


.PHONY: clean
clean:
	-rm  $(target)_arm64.dylib $(target).dylib