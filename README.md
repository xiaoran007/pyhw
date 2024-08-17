# PyHw
PyHw, a neofetch-like command line tool for fetching system information but written mostly in python. Currently, Linux and macOS are supported.

This project is a python reimplementation of [neofetch](https://github.com/dylanaraps/neofetch) and references the [fastfetch](https://github.com/fastfetch-cli/fastfetch) project for logo style settings. Since this project is implemented in python, it will be faster than neofetch's shell implementation and easier to maintain and extend than fastfetch's c implementation. Also, this project only relies on the python standard library, so you can run it on any device that has a python environment (I hope so 🤔)

There are already a lot of similar tools, so you can choose any one of them; they're all essentially no different. If you want to try this tool, just install it directly by pip.
```shell
pip install pyhw
```

## Build from source
### Build tools
Make sure the following python build tools already installed.
* setuptools
* build

### Build package
clone the project, and run:
```shell
python -m build
```
or you can use old setup.py style command:
```shell
python setup.py sdist bdist_wheel
```
After the build process, the source package and the binary whl package can be found in the dist folder.