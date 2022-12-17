from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

setup(ext_modules=cythonize([Extension("lol_graph", ["lol_graph.pyx"],
                                       define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])]),
                             # Extension("cutils", ["cutils.pyx"],
                             #           define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]),
                             # Extension("geno_representation", ["geno_representation.pyx"],
                             #           define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])]),
      include_dirs=[numpy.get_include()],
      requires=['numpy', 'Cython'])
