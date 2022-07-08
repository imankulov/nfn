#!/usr/bin/env python

from distutils.core import setup

setup(
    name="nfn",
    version="0.1",
    description="Generate the next filename.",
    author="Roman Imankulov",
    author_email="roman.imankulov@gmail.com",
    url="https://github.com/imankulov/nfn/",
    py_modules=["nfn"],
    license="MIT",
    scripts=["nfn.py"],
)
