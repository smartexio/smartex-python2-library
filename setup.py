# coding=utf-8
from distutils.core import setup
setup(
    name="smartex",
    packages=["smartex"],
    version="1.0.0",
    description="Accept Ether with Smartex",
    author="Smartex Team",
    author_email="support@smartex.io",
    url="https://github.com/smartexio/smartex-python2-library",
    keywords=["ethereum", "payments", "crypto", "smart contracts"],
    license="MIT License",
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 2 :: Only",
                 "Development Status :: 5 - Production/Stable",
                 "Environment :: Web Environment",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Office/Business :: Financial"],
    long_description="""\
Python Library for integrating with Smartex
-------------------------------------

This library is compatible with Python 2.7.8. It is not compatible with Python 3.

This library is a simple way to integrate your application with
Smartex for taking ethereum payments. It exposes three basic
functions, authenticating with smartex, creating invoices,
and retrieving invoices. It is not meant as a replacement for
the entire Smartex API. However, the key_utils module contains
all of the tools you need to use the Smartex API for other
purposes.

© 2016 Smartex.io Ltd.
"""
)
