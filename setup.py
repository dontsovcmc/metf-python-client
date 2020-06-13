#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Client library for MCU EST Test Framework (METF).
"""

import sys
import platform
from setuptools import setup
from metf_python_client import __version__


cur = 'win32' if sys.platform == 'win32' else platform.linux_distribution()[0].lower()
ext = '.zip' if sys.platform == 'win32' else '.tar.gz'

bin_name = 'metf_python_client-%s-%s%s' % (cur, __version__, ext)


if __name__ == '__main__':

    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setup(
        name='metf-python-client',
        version=__version__,
        description=__doc__.replace('\n', '').strip(),
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Dontsov Evgeny',
        author_email='don-and-home@mail.ru',
        url='https://github.com/dontsovcmc/metf-python-client',
        py_modules=['metf_python_client'],
        include_package_data=True,
        packages=[
            'metf_python_client',
            'metf_python_client.boards',
            'metf_python_client.examples',
        ],
        classifiers=(
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        license='MIT',
        platforms=['linux2', 'win32'],
        install_requires=[
            'requests>=2.22.0',
        ],
    )
