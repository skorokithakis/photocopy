#!/usr/bin/env python
from setuptools import setup
from photocopy.version import VERSION

setup(
    name="photocopy",
    version=VERSION,
    author="Stavros Korokithakis",
    author_email="hi@stavros.io",
    url="https://github.com/skorokithakis/photocopy",
    description="A script to copy images to a directory structure.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=["docopt>=0.6", "exifread>=1.4"],
    packages=["photocopy"],
    entry_points={"console_scripts": ["photocopy = photocopy:main"]},
)
