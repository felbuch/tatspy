# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 21:42:14 2020

@author: Felipe
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tatspy",
    version="0.0.1",
    author="Felipe Buchbinder",
    author_email="felbuch@gmail.com",
    description="Technical Analysis Time Series",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felbuch/tatspy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)