#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy
import os

np_lib = os.path.dirname(numpy.__file__)
np_inc = [os.path.join(np_lib, 'core/include')]

extensions = [
    Extension("dtw.fast",["dtw/fast.pyx"],
        include_dirs=np_inc)
]

setup(name='dtw',
    version='1.0',
    description='Python DTW Module',
    author='Pierre Rouanet',
    author_email='pierre.rouanet@gmail.com',
    url='https://github.com/pierre-rouanet/dtw',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    install_requires=['numpy'],
    packages=find_packages(),
    ext_modules = cythonize(extensions),
)
