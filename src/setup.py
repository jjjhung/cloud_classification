import os
import sys
from setuptools import setup, find_packages

setup(
    name = "Cloud Classification",
    version = "0.0.1",
    author = "Joseph Hung",
    author_email = "joseph.hung@mail.utoronto.ca",
    description = ("Some code to classify Arctic clouds"),
    packages=find_packages(include=['helpers', 'lbldis','processing','readers','visualizations','temp'])
)

sys.path.append('readers')

print(sys.path)