# -*- coding: utf-8 -*-

"""
shitcord.models
~~~~~~~~~~~~~~~

Represents the implementations of the models from the Discord API.
"""

from .base import Model
from .channel import *

__all__ = ['TextChannel', 'DMChannel', 'VoiceChannel', 'GroupDMChannel', 'CategoryChannel']
