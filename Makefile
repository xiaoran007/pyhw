.PHONY: clean, build, upload, install
clean:
	-rm -rf dist/
build: clean
	python -m build
upload:
	twine upload dist/*
install:
	pip install dist/*.whl --force-reinstall