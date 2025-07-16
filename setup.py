#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-image-snapshot',
    version='0.4.4',
    author='Bojan Mihelac',
    author_email='bojan@informatikamihelac.com',
    maintainer='Bojan Mihelac',
    maintainer_email='bojan@informatikamihelac.com',
    license='MIT',
    url='https://github.com/bmihelac/pytest-image-snapshot',
    description='A pytest plugin for image snapshot management and comparison.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['pytest_image_snapshot'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0', 'Pillow'],
    extras_require={
        'pixelmatch': ['pixelmatch>=0.3.0']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'image-snapshot = pytest_image_snapshot',
        ],
    },
)
