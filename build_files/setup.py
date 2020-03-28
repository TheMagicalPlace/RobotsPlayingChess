#!/usr/bin/env python
import os
from distutils.core import setup, Extension
import pybindgen

def generate(file_):
    print(os.getcwd())
    mod = pybindgen.Module('pythonCPPinterop')
    mod.add_include('"CppPythonCrossModule.h"')
    mod.add_function('PythonCPPRunAlphabeta',
                     pybindgen.retval('double'),
                     [pybindgen.param('std::string','boardstring'),
                      pybindgen.param('int','depth'),
                      pybindgen.param('std::string','player')])
    mod.generate(file_)



try:
    os.mkdir("./build_files/build")
except OSError:
    pass
    os.chdir(os.path.join(os.getcwd(),"build_files"))

module_fname = os.path.join("build", "my-module-binding.cpp")
with open(module_fname, "wt") as file_:
    print("Generating file {}".format(module_fname))
    generate(file_)

mymodule = Extension('pythonCPPinterop',
                     sources = [module_fname,
                                '../C++Files/src/CppPythonCrossModule.cpp',
                                '../C++Files/src/alphabeta.cpp',
                                '../C++Files/src/Setup.cpp',
                                '../C++Files/src/ChessPieces.cpp'],
                     include_dirs=['../C++Files/headers'])

setup(name='PyBindGen-example',
      version="0.0",
      description='PyBindGen example',
      author='xxx',
      author_email='yyy@zz',
      ext_modules=[mymodule],

      )

