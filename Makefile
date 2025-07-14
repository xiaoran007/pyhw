.PHONY: lib, clean, build, upload, install, test, docker-run, docker-pypi, test-pypi

lib:
	cd src/pyhw/library/iokitGPULib && make lib
	cd src/pyhw/library/iokitHostLib && make lib
	cd src/pyhw/library/nvmlGPULib && make lib
	cd src/pyhw/library/iokitCPULib && make lib
clean:
	-rm -rf dist/
build: clean lib
	python -m build
upload:
	twine upload dist/*
install:
	pip install dist/*.whl --force-reinstall

docker-local:
	bash scripts/docker_local.sh
docker-pypi:
	bash scripts/docker_pypi.sh

test: build docker-local
test-pypi: docker-pypi