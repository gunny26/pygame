from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("FastMath.pyx", language_level="3")
)
