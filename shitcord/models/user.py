# -*- coding: utf-8 -*-

import enum

from . import abc
from .base import Model

__all__ = ['User']


class RelationshipType(enum.IntEnum):
    FRIEND           = 1
    BLOCKED          = 2
    INCOMING_REQUEST = 3
    OUTGOING_REQUEST = 4


class HypeSquadHouse(enum.IntEnum):
    BRAVERY    = 1
    BRILLIANCE = 2
    BALANCE    = 3


class Flags(enum.IntEnum):
    DISCORD_EMPLOYEE     = 1
    DISCORD_PARTNER      = 2
    DISCORD_HYPESQUAD    = 4
    DISCORD_BUG_HUNTER   = 8
    HYPESQUAD_BRAVERY    = 64
    HYPESQUAD_BRILLIANCE = 128
    HYPESQUAD_BALANCE    = 256
    EARLY_SUPPORTER      = 512


class User(Model, abc.DiscordUser):
    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.username = data['username']
        self.discriminator = data['discriminator']
        self.avatar_hash = data['avatar']
        self.bot = data.get('bot', False)
        self.mfa_enabled = data.get('mfa_enabled', False)
        self.language = data.get('locale')
        self.verified = data.get('verified')
        self.email = data.get('email', '')
        self.flags = data['flags']
        self.premium_type = data.get('premium_type')

    def __str__(self):
        return '{0.username}#{0.discriminator}'.format(self)

    def _has_flag(self, flag):
        value = flag.value
        return (self.flags & value) == value

    @property
    def nitro_classic(self):
        return self.premium_type is not None and self.premium_type == 1

    @property
    def nitro(self):
        return self.premium_type is not None and self.premium_type == 2

    @property
    def employee(self):
        return self._has_flag(Flags.DISCORD_EMPLOYEE)

    @property
    def partner(self):
        return self._has_flag(Flags.DISCORD_PARTNER)

    @property
    def hypesquad(self):
        return self._has_flag(Flags.DISCORD_HYPESQUAD)

    @property
    def bug_hunter(self):
        return self._has_flag(Flags.DISCORD_BUG_HUNTER)

    @property
    def hypesquad_house(self):
        houses = [
            house for house, flag in zip(HypeSquadHouse, (Flags.HYPESQUAD_BRAVERY, Flags.HYPESQUAD_BRILLIANCE, Flags.HYPESQUAD_BALANCE))
            if self._has_flag(flag)
        ]

        if len(houses) == 1:
            return houses[0]
        return houses
