# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
   GWCS - Generalized World Coordinate System
   ==========================================


Generalized World Coordinate System (GWCS) is an Astropy affiliated package
providing tools for managing the World Coordinate System of astronomical data.

GWCS takes a general approach to the problem of expressing transformations between
pixel and world coordinates. It supports a data model which includes the entire
transformation pipeline from input coordinates (detector by default) to world
coordinates. It is tightly integrated with Astropy.

- Transforms are instances of ``astropy.Model``. They can be chained, joined or
  combined with arithmetic operators using the flexible framework of
  compound models in ``astropy.modeling``.
- Celestial coordinates are instances of ``astropy.SkyCoord`` and are transformed
  to other standard celestial frames using ``astropy.coordinates``.
- Time coordinates are represented by ``astropy.Time`` and can be further manipulated
  using the tools in ``astropy.time``
- Spectral coordinates are ``astropy.Quantity`` objects and can be converted to other
  units using the tools in ``astropy.units``.

For complete features and usage examples see the documentation site:

http://gwcs.readthedocs.org

Note
----

GWCS supports only Python 3.


Installation
------------

To install::

    pip install gwcs

To clone from github and install the master branch::

    git clone https://github.com/spacetelescope/gwcs.git
    cd gwcs
    python setup.py install


Contributing Code, Documentation, or Feedback
---------------------------------------------

GWCS is developed on github. We welcome feedback and contributions to the project.
Contributions of code, documentation, or general feedback are all appreciated. More
information about contributing is in the github repository.


"""

import sys
if sys.version_info < (3, 5):
    raise ImportError("GWCS does not support Python 2.x, 3.0, 3.1, 3.2, 3.3 or 3.4."
                      "Beginning with GWCS 0.9, Python 3.5 and above is required.")


# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import * # noqa
# ----------------------------------------------------------------------------


# For egg_info test builds to pass, put package imports here.
if not _ASTROPY_SETUP_:
    from .wcs import *   # noqa
    from .wcstools import *   # noqa
    from .coordinate_frames import *  # noqa
    from .selector import *   # noqa
