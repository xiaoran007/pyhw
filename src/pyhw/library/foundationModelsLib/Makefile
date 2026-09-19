# These SDK/toolchain settings are local to this library.
FOUNDATION_MODELS_SDK ?= macosx27.0
FOUNDATION_MODELS_DEVELOPER_DIR ?= $(shell xcode-select -p)
SDK_PATH = $(shell DEVELOPER_DIR="$(FOUNDATION_MODELS_DEVELOPER_DIR)" xcrun --sdk $(FOUNDATION_MODELS_SDK) --show-sdk-path)
SWIFTC = DEVELOPER_DIR="$(FOUNDATION_MODELS_DEVELOPER_DIR)" xcrun --sdk $(FOUNDATION_MODELS_SDK) swiftc
MODULE_CACHE ?= $(CURDIR)/build/module-cache
FLAGS = -sdk "$(SDK_PATH)" -module-cache-path "$(MODULE_CACHE)" -framework FoundationModels
TARGET = foundationModelsLib

.PHONY: lib clean
lib:
	mkdir -p build ../lib
	$(SWIFTC) -emit-library $(TARGET).swift $(FLAGS) -target arm64-apple-macos26.0 -o build/$(TARGET)_arm64.dylib
	$(SWIFTC) -emit-library $(TARGET).swift $(FLAGS) -target x86_64-apple-macos26.0 -o build/$(TARGET)_x86_64.dylib
	lipo -create build/$(TARGET)_arm64.dylib build/$(TARGET)_x86_64.dylib -output ../lib/$(TARGET).dylib

clean:
	rm -rf build
	rm -f ../lib/$(TARGET).dylib
