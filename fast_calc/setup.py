'''
Created on Jul 1, 2013

@author: dmasad
'''

from distutils.core import setup
from Cython.Build import cythonize

setup(
      name="fast_calc",
      ext_modules=cythonize("fast_calc.pyx"),
)
