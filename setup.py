from distutils.core import setup, Extension

from os import getenv
import sys
import os
import shutil

p = sys.prefix
NUMPYPATH = '.'
if os.path.isdir(p + '/include/numpy'):
  NUMPY = 'NUMPY'
elif os.path.isdir(p + '/Lib/site-packages/numpy/core/include/numpy'):
  NUMPY = 'NUMPY'
  NUMPYPATH = p + '/Lib/site-packages/numpy/core/include'
elif os.path.isdir(p + '/lib/python3.6/site-packages/numpy/core/include/numpy'):
  NUMPY = 'NUMPY'
  NUMPYPATH = p + '/lib/python3.6/site-packages/numpy/core/include'
else:
  NUMPY = 'NONUMPY'
print ('numpy: ' + NUMPY)
windir = getenv('windir')
if windir == None:
  WIN32 = 'NOWIN32'
  LPSOLVE55 = 'lpsolve55/bin/ux64'
  LPSOLVE55_PATH = '%s/liblpsolve55.so' % LPSOLVE55
  shutil.copyfile(LPSOLVE55_PATH, '/usr/lib')
else:
  WIN32 = 'WIN32'
  LPSOLVE55 = 'lpsolve55/bin/win32'
  LPSOLVE55_PATH = '%s/lpsolve55.dll' % LPSOLVE55
  LPSOLVE55_FILENAME = os.path.basename(LPSOLVE55_PATH)
  shutil.copyfile(LPSOLVE55_PATH, LPSOLVE55_FILENAME)


setup (name = "lpsolve55",
       version = "5.5.2.5",
       description = "Linear Program Solver, Interface to lpsolve",
       author = "Peter Notebaert",
       author_email = "lpsolve@peno.be",
       url = "http://www.peno.be/",
       packages=[''],
       package_dir={'': '.'},
       package_data={'': ['*.dll', '*.so', 'lp_solve.py', 'lp_maker.py']},
       #py_modules=['extra/Python/lp_solve', 'extra/Python/lp_maker'],
       ext_modules = [Extension("lpsolve55",
				["extra/Python/lpsolve.c", "extra/Python/hash.c", "extra/Python/pythonmod.c"],
                                define_macros=[('PYTHON', '1'), (WIN32, '1'), ('NODEBUG', '1'), ('DINLINE', 'static'), (NUMPY, '1'), ('_CRT_SECURE_NO_WARNINGS', '1')],
                                include_dirs=['../..', NUMPYPATH, LPSOLVE55],
                                library_dirs=[LPSOLVE55],
				libraries = ["lpsolve55"])
		      ]
)


try:
    if LPSOLVE55_FILENAME:
        os.remove(LPSOLVE55_FILENAME)
    shutil.rmtree('build')
except:
    pass
