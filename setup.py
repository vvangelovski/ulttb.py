from setuptools import setup
from setuptools.extension import Extension

ULTTB_VERSION = '0.1.0'

cmdclass = { }
ext_modules = [ ]

ext_modules += [
    Extension("ulttb._lttb", [ "src/_lttb.c" ]),
]

setup(
    name='ulttb',
    version=ULTTB_VERSION,
    cmdclass = cmdclass,
    package_dir={'ulttb': './src', 'ulttb.tests': './tests'},
    packages=['ulttb', 'ulttb.tests'],
    ext_modules=ext_modules,
)
