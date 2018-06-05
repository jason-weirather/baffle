from setuptools import setup, find_packages
from codecs import open
from os import path
import sys

this_folder = path.abspath(path.dirname(__file__))
with open(path.join(this_folder,'README.md'),encoding='utf-8') as inf:
  long_description = inf.read()

setup(
  name='baffle',
  version='1.0.0',
  description='Python tools for adding randomized / imputed fake data to hide real data. Specifically geared to expressiond data.',
  long_description=long_description,
  url='https://github.com/jason-weirather/baffle',
  author='Jason L Weirather',
  author_email='jason.weirather@gmail.com',
  license='Apache License, Version 2.0',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: Apache Software License'
  ],
  keywords='bioinformatics, expression',
  packages=['baffle'
           ]
)
