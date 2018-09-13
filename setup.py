# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typestruct",
    version="0.1.0",
    author="Zeyi Fan",
    author_email="i@zr.is",
    description="A easier way to use struct",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fanzeyi/typestruct",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
