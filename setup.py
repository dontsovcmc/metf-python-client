#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Client library for MCU EST Test Framework (METF).
"""

from setuptools import setup, find_packages
from metf_python_client import __version__


if __name__ == '__main__':

    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

    setup(
        name='metf-python-client',
        version=__version__,
        description='HTTP client library for testing hardware using ESP boards (NodeMCU, WeMos, ESP32C6)',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Evgeny Dontsov',
        author_email='don-and-home@mail.ru',
        url='https://github.com/dontsovcmc/metf-python-client',
        project_urls={
            'Documentation': 'https://github.com/dontsovcmc/metf-python-client#readme',
            'Source': 'https://github.com/dontsovcmc/metf-python-client',
            'Tracker': 'https://github.com/dontsovcmc/metf-python-client/issues',
        },
        packages=find_packages(),
        include_package_data=True,
        python_requires='>=3.7',
        install_requires=[
            'requests>=2.22.0',
        ],
        extras_require={
            'dev': [
                'pytest>=7.0',
                'pytest-cov>=4.0',
                'black>=23.0',
                'flake8>=6.0',
                'mypy>=1.0',
            ],
        },
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Testing",
            "Topic :: System :: Hardware",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Operating System :: OS Independent",
        ],
        keywords='esp8266 esp32 nodemcu wemos hardware testing iot embedded continuous-integration i2c gpio',
        license='MIT',
        zip_safe=False,
    )
