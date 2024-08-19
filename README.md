# PyHw
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyhw?label=PyPI)


PyHw, a neofetch-like command line tool for fetching system information but written mostly in Python. **Currently, this project is still in the initial stage, only part of the linux systems are supported. macOS support will be added soon.**

This project is a Python reimplementation of [neofetch](https://github.com/dylanaraps/neofetch) and references the [fastfetch](https://github.com/fastfetch-cli/fastfetch) project for logo style settings. Since this project is implemented in Python, it will be easier to maintain and extend than bash and c implementation. Also, this project only relies on the Python standard library, so you can run it on any device that has a Python environment (I hope so 🤔)

There are already a lot of similar tools so you can choose any of them; they're all essentially no different. If you want to try this tool, just install it directly by pip.
```shell
pip install pyhw
```
You can then use this tool directly from the command line with the following command, just like neofetch.
```shell
pyhw
```

## Build from source
### Build tools
Make sure the following Python build tools are already installed.
* setuptools
* build
* twine

### Build package
clone the project, and run:
```shell
python -m build
```
or you can use the old setup.py style command:
```shell
python setup.py sdist bdist_wheel
```
After the build process, the source package and the binary whl package can be found in the dist folder.