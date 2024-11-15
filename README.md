# PyHw
[![Downloads](https://static.pepy.tech/badge/pyhw)](https://pepy.tech/project/pyhw)
![PyPI - Version](https://img.shields.io/pypi/v/pyhw?label=version)

![Static Badge](https://img.shields.io/badge/macOS-11%2B-green
)
![Static Badge](https://img.shields.io/badge/Linux-blue)


PyHw, a neofetch-like command line tool for fetching system information but written mostly in Python. **Currently, this project is still in the initial stage, only part of the linux systems and macOS are supported.**

This project is a Python reimplementation of [neofetch](https://github.com/dylanaraps/neofetch) and references the [fastfetch](https://github.com/fastfetch-cli/fastfetch) project for logo style settings. Since this project is implemented in Python, it will be easier to maintain and extend than bash and c implementation. Also, this project only relies on the Python standard library, so you can run it on any device that has a Python environment (I hope so 🤔).


[//]: # (![demo]&#40;https://i2.imgs.ovh/d/BQACAgUAAx0EUvSR8wACMvpmyFVohzKxLcUdLiJaEa3wlo_OrQACuw4AAoX-QVaSpG0-rTAeRTUE&#41;)
![demo](https://files.catbox.moe/xx58xy.jpg)





## Install
There are already a lot of similar tools so you can choose any of them; they're all essentially no different. If you want to try this tool, just install it directly by pip.
```shell
pip install pyhw
```
To upgrade pyhw:
```shell
pip install pyhw -U
# or
pip install pyhw --upgrade
```
You can then use this tool directly from the command line with the following command, just like neofetch.
```shell
pyhw
```
Please note that the command line entry for __pyhw__ is created by pip, and depending on the user, this entry may not in the __system PATH__. If you encounter this problem, pip will give you a prompt, follow the prompts to add entry to the __system PATH__.

### Install by pipx
**pipx** is an amazing tool to help you install and run applications written in Python. It is more like **brew** or **apt**. You can find more information about it here [pipx](https://github.com/pypa/pipx).

You can install pyhw by the following command:
```shell
pipx install pyhw
```
You can then use this tool directly from the command line with the following command, just like neofetch.
```shell
pyhw
```

### Important note about debian 12:
If you use system pip to install pyhw, you will encounter this problem on debian12 and some related distributions:
```text
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```
This is due to the fact that system python is not supposed to be managed by pip. You can simply use **pipx** to install **pyhw**. Or you can use a virtual environment (venv) or force remove this restriction (not recommended).

## Supported (Tested) OS
* macOS arm64, x86_64
* debian-based distro arm64, x86_64
* RaspberryPi OS arm64


## Build from source
Currently, build process relay on swiftc and macOS IOKit framework. To build package from source, you need a mac machine with macOS 11 and newer.

### Dependencies
This package was originally implemented in pure python and only depends on the python standard library. However, in subsequent development, the code for the pci part was separated into a separate package **pypci-ng**, which can be obtained using pip (or check out [this](https://github.com/xiaoran007/pypci) GitHub repository).

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
After the build process, the source package and the binary whl package can be found in the dist folder. Then you can use the following command to install the new package.
```shell
pip install dist/*.whl --force-reinstall
```
Or simply type:
```shell
make build
make install
```
