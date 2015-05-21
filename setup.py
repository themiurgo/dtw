#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='dtw',
    version='1.0',
    description='Python DTW Module',
    author='Pierre Rouanet',
    author_email='pierre.rouanet@gmail.com',
    url='https://github.com/pierre-rouanet/dtw',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    install_requires=['numpy'],
    packages=find_packages(),
)
