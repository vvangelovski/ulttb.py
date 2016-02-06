from setuptools import setup
from setuptools.extension import Extension

ULTTB_VERSION = '0.1.0'

cmdclass = { }
ext_modules = [ ]

ext_modules += [
    Extension("ulttb._lttb",
              sources= [ "./src/_lttb.c" ],
              include_dirs = ['./src',],
              extra_compile_args=['-D_GNU_SOURCE', '-O2']
              ),
]

setup(
    name='ulttb',
    author='Vasil Vangelovski',
    author_email='vvangelovski@gmail.com',
    version=ULTTB_VERSION,
    cmdclass = cmdclass,
    package_dir={'ulttb': './src', 'ulttb.tests': './tests'},
    packages=['ulttb', 'ulttb.tests'],
    ext_modules=ext_modules,
    platforms=['any'], 
)
