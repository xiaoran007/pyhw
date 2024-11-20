.PHONY: lib, clean, build, upload, install, test, docker-run, docker-pypi

lib:
	cd src/pyhw/library/iokitGPULib && make lib
clean:
	-rm -rf dist/
build: clean lib
	python -m build
upload:
	twine upload dist/*
install:
	pip install dist/*.whl --force-reinstall

docker-local:
	docker run --rm \
		-v $(shell pwd)/dist:/app/dist \
		python:3.9-slim bash -c "\
			pip install /app/dist/*.whl && \
			pyhw"
docker-pypi:
	docker run --rm \
		python:3.9-slim bash -c "\
			pip install pyhw -U && \
			pyhw"
test: build docker-local
test-pypi: docker-pypi