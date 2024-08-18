.PHONY: clean, build, upload
clean:
	-rm -rf dist/
build: clean
	python -m build
upload:
	twine upload dist/*