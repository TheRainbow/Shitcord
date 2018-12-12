# -*- coding: utf-8 -*-

import enum

from .core import Model


class StatusType(enum.Enum):
    ONLINE         = 'online'
    DND            = 'dnd'
    IDLE           = 'idle'
    INVISIBLE      = 'invisible'
    OFFLINE        = 'offline'


class ActivityType(enum.IntEnum):
    PLAYING   = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING  = 3


class Activity(Model):
    """
    Represents an Activity model from the Discord API that will be used
    for allowing bot accounts to change their presence on Discord.
    """

    def __init__(self, *, name='', activity_type=ActivityType.PLAYING, url=None):
        __slots__ = ('name', 'type', 'url')

        super().__init__(0, None)  # Just a stub.

        self.name = name
        self.type = activity_type.value
        self.url = url

    def to_json(self):
        # Streaming always requires a valid url.
        if self.type == 1 and self.url is None:
            raise ValueError('Streaming status isn\'t allowed without a valid twitch.tv url provided.')

        return {
            'name': self.name,
            'type': self.type,
            'url': self.url,
        }
