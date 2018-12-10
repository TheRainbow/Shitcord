# -*- coding: utf-8 -*-

"""
shitcord.http
~~~~~~~~~~~~~

Represents the generic wrapper for the Discord REST API.
This provides utility for interfacing with the API, parsing the responses,
tracking requests and handling rate limits.
"""

from .errors import ShitRequestFailed
from .http import HTTP
from .rate_limit import Limiter
from .routes import Endpoints

__all__ = []
