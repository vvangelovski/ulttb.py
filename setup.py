import sys
from setuptools import setup
from setuptools.extension import Extension

ULTTB_VERSION = '0.1.0'

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.1
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: C
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Scientific/Engineering :: Visualization
Operating System :: Microsoft :: Windows
Operating System :: Unix
"""

PLATFORM_IS_WINDOWS = sys.platform.lower().startswith('win')


cmdclass = { }
ext_modules = [ ]
define_macros = []
version_flags = []

if version_flags:
    ULTTB_VERSION_EX = ULTTB_VERSION + " (%s)" % ' '.join(version_flags)
else:
    ULTTB_VERSION_EX = ULTTB_VERSION

if not PLATFORM_IS_WINDOWS:
    define_macros.append(('ULTTB_VERSION', '"' + ULTTB_VERSION_EX + '"'))
else:
    define_macros.append(('ULTTB_VERSION', '\\"' + ULTTB_VERSION_EX + '\\"'))


ext_modules += [
    Extension("ulttb._lttb",
              sources= [ "./src/_lttb.c" ],
              include_dirs = ['./src',],
              define_macros=define_macros,
              extra_compile_args=['-D_GNU_SOURCE', '-O2']
              ),
]

setup(
    name='ulttb',
    author='Vasil Vangelovski',
    author_email='vvangelovski@gmail.com',
    version=ULTTB_VERSION,
    classifiers=[x for x in classifiers.split("\n") if x],
    cmdclass = cmdclass,
    package_dir={'ulttb': './src', 'ulttb.tests': './tests'},
    packages=['ulttb', 'ulttb.tests'],
    ext_modules=ext_modules,
    platforms=['any'],
)
