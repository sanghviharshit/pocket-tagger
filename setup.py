import subprocess
import sys
import os

from os import path
from io import open
from setuptools import setup

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pocket-tagger',
    version='0.1.0',
    description='Tag your pocket articles from getpocket.com automatically using NLP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/sanghviharshit/pocket-tagger',
    author='Harshit Sanghvi',
    author_email='hello@sanghviharshit.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    keywords='getpocket, pocket, api, articles, automatic, suggested, tag, natural language processing, nlp',
    packages=['pocket_tagger'],
    install_requires=['google.cloud', 'pocket', 'requests', 'bs4'],
    project_urls={
        'Bug Reports': 'https://github.com/sanghviharshit/pocket-tagger/issues',
        'Say Thanks!': 'https://saythanks.io/to/sanghviharshit',
        'Source': 'https://github.com/sanghviharshit/pocket-tagger',
    },
)
