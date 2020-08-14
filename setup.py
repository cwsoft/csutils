"""
#######################################################################################
# Setup script for installing the csutils package via Python pip or setuptools.
#
# @package: csutils
# @repo:    https://github.com/cwsoft/csutils
# @author:  cwsoft
# @python:  3.8 or higher
#######################################################################################
"""
import setuptools

setuptools.setup(
    name="csutils",
    version="1.0.0",
    author="cwsoft",
    author_email="noreply@cwsoft.de",
    description="Collection of modules to ease tasks like dealing with textfiles, manipulate terminal colors and cursor.",
    long_description="Visit Github repository to learn more about the csutils package.",
    long_description_content_type="text/markdown",
    url="https://github.com/cwsoft/csutils",
    packages=setuptools.find_packages(exclude=["tests", "docs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
