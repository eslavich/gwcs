#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import glob
import os
import sys
import builtins

import ah_bootstrap
from setuptools import setup

if sys.version_info < (3, 4):
    error = """
    GWCS 0.9+ does not support Python 2.x, 3.0, 3.1, 3.2, 3.3 or 3.4.
    Beginning with GWCS 0.9, Python 3.5 and above is required.

    This may be due to an out of date pip

    Make sure you have pip >= 9.0.1.

    """
    sys.exit(error)

builtins._ASTROPY_SETUP_ = True

from astropy_helpers.setup_helpers import (
    register_commands, adjust_compiler, get_debug_option, get_package_info)
from astropy_helpers.git_helpers import get_git_devstr
from astropy_helpers.version_helpers import generate_version_py

# Get some values from the setup.cfg
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
conf = ConfigParser()
conf.read(['setup.cfg'])
metadata = dict(conf.items('metadata'))

PACKAGENAME = metadata.get('package_name', 'packagename')
DESCRIPTION = metadata.get('description', 'Astropy affiliated package')
AUTHOR = metadata.get('author', '')
AUTHOR_EMAIL = metadata.get('author_email', '')
LICENSE = metadata.get('license', 'unknown')
URL = metadata.get('url', 'http://astropy.org')

# Get the long description from the package's docstring
__import__(PACKAGENAME)
package = sys.modules[PACKAGENAME]
LONG_DESCRIPTION = package.__doc__

# Store the package name in a built-in variable so it's easy
# to get from other parts of the setup infrastructure
builtins._ASTROPY_PACKAGE_NAME_ = PACKAGENAME

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)

VERSION = '0.9.0'

# Indicates if this version is a release version
RELEASE = 'dev' not in VERSION

if not RELEASE:
    VERSION += get_git_devstr(False)

# Populate the dict of setup command overrides; this should be done before
# invoking any other functionality from distutils since it can potentially
# modify distutils' behavior.
cmdclassd = register_commands(PACKAGENAME, VERSION, RELEASE)

# Freeze build information in version.py
generate_version_py(PACKAGENAME, VERSION, RELEASE,
                    get_debug_option(PACKAGENAME))

# Treat everything in scripts except README.rst as a script to be installed
scripts = [fname for fname in glob.glob(os.path.join('scripts', '*'))
           if os.path.basename(fname) != 'README.rst']


# Get configuration information from all of the various subpackages.
# See the docstring for setup_helpers.update_package_files for more
# details.
package_info = get_package_info()

def get_package_data():
    # Installs the schema files
    schemas = []
    root = os.path.join(PACKAGENAME, 'schemas')
    for node, dirs, files in os.walk(root):
        for fname in files:
            if fname.endswith('.yaml'):
                schemas.append(
                    os.path.relpath(os.path.join(node, fname), root))
    # In the package directory, install to the subdirectory 'schemas'
    schemas = [os.path.join('schemas', s) for s in schemas]
    return schemas

schemas = get_package_data()

# Add the project-global data
package_info['package_data'].setdefault(PACKAGENAME, schemas)
package_info['package_data'][PACKAGENAME].append('data/*')

# Include all .c files, recursively, including those generated by
# Cython, since we can not do this in MANIFEST.in with a "dynamic"
# directory name.
c_files = []
for root, dirs, files in os.walk(PACKAGENAME):
    for filename in files:
        if filename.endswith('.c'):
            c_files.append(
                os.path.join(
                    os.path.relpath(root, PACKAGENAME), filename))
package_info['package_data'][PACKAGENAME].extend(c_files)

entry_points = dict(asdf_extensions='gwcs = gwcs.extension:GWCSExtension')

setup(name=PACKAGENAME,
      version=VERSION,
      description=DESCRIPTION,
      scripts=scripts,
      entry_points=entry_points,
      requires=['astropy', 'asdf'],
      python_requires='>=3.5',
      install_requires=['astropy', 'asdf'],
      provides=[PACKAGENAME],
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      long_description=LONG_DESCRIPTION,
      cmdclass=cmdclassd,
      zip_safe=False,
      use_2to3=False,
      **package_info
)
