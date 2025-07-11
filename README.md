# PyHw, a neofetch-like system information fetching tool
[![Downloads](https://static.pepy.tech/badge/pyhw)](https://pepy.tech/project/pyhw)
![PyPI - Version](https://img.shields.io/pypi/v/pyhw?label=version)
![Static Badge](https://img.shields.io/badge/Python-3.9%2B-green)

![Static Badge](https://img.shields.io/badge/macOS-11%2B-green)
![Static Badge](https://img.shields.io/badge/Linux-blue)
![Static Badge](https://img.shields.io/badge/FreeBSD-red)
![Static Badge](https://img.shields.io/badge/Windows-yellow)

![Static Badge](https://img.shields.io/badge/amd64-green)
![Static Badge](https://img.shields.io/badge/aarch64-blue)
![Static Badge](https://img.shields.io/badge/arm32-yellow)
![Static Badge](https://img.shields.io/badge/riscv64-%238A2BE2)
![Static Badge](https://img.shields.io/badge/ppc64-orange)
![Static Badge](https://img.shields.io/badge/s390x-red)


PyHw, a neofetch-like command line tool for fetching system information but written mostly in Python.

This project is a Python reimplementation of [neofetch](https://github.com/dylanaraps/neofetch) and references the [fastfetch](https://github.com/fastfetch-cli/fastfetch) project for logo style settings. Since this project is implemented in Python, it will be easier to maintain and extend than bash and c implementation. Also, this project only relies on the Python standard library, so you can run it on any device that has a Python environment (I hope so 🤔).


[//]: # (![demo]&#40;https://i2.imgs.ovh/d/BQACAgUAAx0EUvSR8wACMvpmyFVohzKxLcUdLiJaEa3wlo_OrQACuw4AAoX-QVaSpG0-rTAeRTUE&#41;)
[//]: # (![demo]&#40;https://files.catbox.moe/xx58xy.jpg&#41;)
[//]: # (![demo]&#40;https://files.catbox.moe/2d21fu.jpg&#41;)

![demo](https://files.catbox.moe/ik4ioi.png)


- [1. Install](#1-install)
- [2. Usability](#2-usability)
- [3. Add Logo](#3-add-logo)
- [4. Build from source](#4-build-from-source)
- [5. Test Package](#5-test-package)
- [6. Troubleshooting](#6-troubleshooting)


## 1. Install
There are already a lot of similar tools so you can choose any of them; they're all essentially no different. If you want to try this tool, There are two convenient ways to install it.

### 1.1 Install by pipx
**pipx** is an amazing tool to help you install and run applications written in Python. It is more like **brew** or **apt**. You can find more information about it here [pipx](https://github.com/pypa/pipx). **pipx** is available on almost all major platforms and is usually provided by the corresponding package manager. If you haven't used pipx before, you can refer to this [document](https://pipx.pypa.io/stable/installation/) to install it.

You can install pyhw by the following command:
```shell
pipx install pyhw
```
You can then use this tool directly from the command line with the following command, just like neofetch.
```shell
pyhw
```

### 1.2 Install by pip
In any case, pip is always available, so if you can't install this program using **pipx**, you can install pyhw by the following command:
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
# or
python -m pyhw
```
Please note that the command line entry for __pyhw__ is created by pip, and depending on the user, this entry may not in the __system PATH__. If you encounter this problem, pip will give you a prompt, follow the prompts to add entry to the __system PATH__.


## 2. Usability
### Tested Platform
The following platforms have been tested and are known to work with this package:
* macOS: arm64, x86_64
* Linux: arm64, x86_64, riscv64, ppc64le, mips64el, s390x
* FreeBSD: arm64, x86_64
* Windows 10: x86_64
* Windows 11: arm64, x86_64

For more detailed information, please refer to [Tested Platform](docs/tested_platform.md).

Please note that this package requires `Python 3.9`, so very old versions of Linux may not be supported.

### Features
The functionality of this package varies slightly on different operating systems and architectures, please refer to [this](docs/functionality.md) documentation for details.

## 3. Add Logo
1. Create a file named **\<os>.pyhw** in **logo/ascii** folder
2. Modify **colorConfig.py** file to add a new logo style
3. Update **pyhwUtil.py** to enable new logo style.
4. You may create a new `PR` to add your logo style to the main repository.

## 4. Build from source

### 4.1 Dependencies
This package was originally implemented in pure python and only depends on the python standard library. However, in subsequent development, the code for the pci part was separated into a separate package **pypci-ng**, which can be obtained using pip (or check out [this](https://github.com/xiaoran007/pypci) GitHub repository).

### 4.2 Build tools
Make sure the following Python build tools are already installed.
* setuptools
* build
* twine

Newer versions of twine requires the following dependencies are up to date:
* setuptools
* build
* twine
* packaging

### 4.3 Build package
clone the project, and run:
```shell
python -m build
```
After the build process, the source package and the binary whl package can be found in the dist folder. Then you can use the following command to install the new package.
```shell
pip install dist/*.whl --force-reinstall
```

### 4.4 Build Full Feature package
Currently, build process relay on swiftc and macOS IOKit framework. To build Full Feature Package from source, you need a Mac machine with macOS 11 and newer.

Simply type:
```shell
make build
make install
```

## 5. Test Package
If you have docker installed, you can test this package through docker by type:
```shell
make test # local build
make test-pypi # release version
```

## 6. Troubleshooting
### 6.1 Important note about debian 12:
If you use system pip to install pyhw, you will encounter this problem on debian12 and some related distributions (like Ubuntu 24.04):
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
This is due to the fact that system python is not supposed to be managed by pip. You can simply use **pipx** to install **pyhw**. Or you can use a virtual environment (venv), conda environment or force remove this restriction (not recommended).
