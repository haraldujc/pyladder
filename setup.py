# Setup package:
# https://setuptools.readthedocs.io/en/latest/setuptools.html

# Python packaging user guide
# https://packaging.python.org/tutorials/packaging-projects/

# Pypi install
# https://packaging.python.org/tutorials/installing-packages/

# Install packaging packages
# python3 -m pip install --user --upgrade setuptools wheel
# python3 -m pip install --user --upgrade twine

# test pypi
# Package pyladder and upload to test pypi (python package index)
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# And here it is
# https://test.pypi.org/project/pyladder/0.0.1/

# Now install locally
# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-your-username

# Test with python from the command line
# >>import pyladder
# >>ladder_edge_list = [[10,20], [10,30], [10,40], [10,50], [20,30], [20,40], [20,50], [30,40], [40,50]]
# >>my_ladder = pyladder.Pyladder()
# >>my_ladder.display_graph_plot_edges('Nodes', 'dictionary input', ladder_edge_list)

# pypi
# python3 -m twine upload dist/*
# And here it is
# https://pypi.org/project/pyladder/0.0.1/


import os
import sys

import setuptools
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

classifiers = [
        #'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics']

sourcefiles = ['pyladder.py']

setuptools.setup(
    name='pyladder',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=False,
    # scripts=['pyladder.py'],
    author='Harald Ujc',
    author_email='harald.ujc@screenpopsoftware.com',
    maintainer='Harald ujc',
    maintainer_email='harald.ujc@screenpopsoftware.com',
    description='A python package for planarity testing and rendering of ladder type graphs',
    classifiers=classifiers,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haraldujc/pyladder',
    python_requires='>=3.6',
)