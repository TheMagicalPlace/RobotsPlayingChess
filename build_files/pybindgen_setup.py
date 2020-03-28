import pybindgen
from pybindgen.typehandlers import stringtype
import os
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

if __name__ == '__main__':
    pass