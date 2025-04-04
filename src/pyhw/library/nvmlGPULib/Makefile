.PHONY: lib, clean, docker_build

lib: docker_build
	@echo "Building nvmlGPULib"
	mkdir -p ../lib
	cp out/linux_amd64/nvmlGPULib.so ../lib/nvmlGPULib_amd64.so
	cp out/linux_arm64/nvmlGPULib.so ../lib/nvmlGPULib_arm64.so
	@echo "nvmlGPULib built and copied to ../lib"
	@echo "Cleaning temp files"
	rm -rf out



docker_build:
	@echo "Building nvmlGPULib by docker"
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--output type=local,dest=./out \
		.

clean:
	@echo "Cleaning temp files"
	rm -rf out
