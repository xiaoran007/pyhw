from setuptools import setup, find_packages

setup(
    name="pyhw",
    version="0.1.0b",
    author="Xiao Ran",
    author_email="xiaoran.007@icloud.com",
    description="PyHw, a neofetch-like command line tool for fetching system information but written mostly in python.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xiaoran007/pyhw",
    license="BSD-3-Clause",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyhw=pyhw.__main__:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[],
)
