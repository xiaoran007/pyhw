.PHONY: lib, clean, build, upload, install
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