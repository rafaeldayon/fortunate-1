# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

from fortunate import __version__, __author__, __email__, __url__, __license__


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname), "r") as fp:
            return fp.read().strip()
    except IOError:
        return ''


setup(
    name="fortunate",
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    description="Python version of old BSD Unix fortune program",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Filters",
    ],
    packages=['fortunate'],
    package_data={'fortunate': ['fortunes']},
    entry_points={
        'console_scripts': [
            'fortunate = fortunate.__init__:main'
        ]
    },
)
