from setuptools import setup
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Jackson Rakena",
    author_email="jackson@rakena.co.nz",
    name="migadu-cli",
    url="https://github.com/jacksonrakena/migadu-cli",
    description="Command line tool for managing Migadu email hosting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['migadu-cli'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        mictl=mictl:mictl
    ''',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Environment :: Console"
    ]
)