# -*- coding: utf-8 -*-

"""
Shitcord
----------

A shitty, fucked up wrapper of the Discord API.
Don't expect too much because this was intended to be a joke at the beginning. :^)
Though I think this lib could actually be pretty cool...

:copyright: (c) 2018 Valentin B.
:license: GNU GPLv3, see LICENSE for more information
"""

# This has to be here because otherwise it may cause issues
from gevent import monkey
monkey.patch_all()

import logging
import sys
from collections import namedtuple

from .http.api import API
from .utils.snowflake import *
from .models import *
from .gateway import *
from .client import Client

__title__ = 'Shitcord'
__author__ = 'Valentin B.'
__version__ = '0.0.2b'
__license__ = 'GNU GPLv3'
__copyright__ = '(c) 2018 Valentin B.'
__url__ = 'https://github.com/itsVale/Shitcord'

Version = namedtuple('VersionInfo', 'major minor micro releaselevel')
version_info = Version(major=0, minor=0, micro=2, releaselevel='beta')

fmt = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)

# To support Python versions under 3.6.1, we need to implement our own NullHandler
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

if sys.version_info < (3, 4):
    raise RuntimeError('Upgrade your Python, you shitter.')
