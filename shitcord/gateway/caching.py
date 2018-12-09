# -*- coding: utf-8 -*-

from ..models.guild import Guild


def store(client, obj):
    if isinstance(obj, Guild):
        client._store_guild(obj)
