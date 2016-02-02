from setuptools import setup
from setuptools.extension import Extension

ULTTB_VERSION = '0.1.0'

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = { }
ext_modules = [ ]

if use_cython:
    ext_modules += [
        Extension("ulttb._lttb", [ "src/_lttb.pyx" ]),
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
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