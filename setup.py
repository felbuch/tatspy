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
    version="0.1.0",
    author="Felipe Buchbinder",
    author_email="felbuch@gmail.com",
    description="Technical Analysis Time Series for Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ['STOCK', 'TECHNICAL ANALYSIS INDICATORS', 'HISTORICAL DATA' ,'TIME SERIES', 'MACHINE LEARNING', 'ALGORITHMIC TRADING'],   
    download_url='https://github.com/felbuch/tatspy/archive/v0.1.0.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=['numpy','pandas','datetime','investpy','ta']
)