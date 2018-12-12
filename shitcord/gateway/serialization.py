# -*- coding: utf-8 -*-

import platform


def identify(token, name, compress=True, large_threshold=50, *, shard=None, presence=None):
    """
    Returns a payload in JSON format for identifying.

    :param token:
        The bot's token.
    :param name:
        The library's name.
    :param compress:
        Whether the connection supports compression of the packages.
    :param large_threshold:
        Value between 50 and 250, total number of members where the gateway
        will stop sending offline members in the guild member list.
    :param shard:
        A list with 2 values indicating the shard to use and the total amount of shards.
    :param presence:
        An `Update Status` object that should be sent.

    :return:
        An OPCode 2 payload in JSON format for identifying.
    """

    # Defining the default values for bots that use this Gateway client if no custom one is provided.
    presence = presence or {'since': None, 'game': None, 'status': 'online', 'afk': False}
    shard = shard or [0, 1]

    return {
        'token': token,
        'properties': {
            '$os': platform.system(),
            '$browser': name,
            '$device': name
        },
        'compress': compress,
        'large_threshold': large_threshold,
        'shard': shard,
        'presence': presence
    }


def resume(token, session_id, seq):
    """
    Returns a payload in JSON format used to reconnect when a client needs to be reconnected.

    :param token:
        The bot's token.
    :param session_id:
        The session_id for the corresponding session that should be resumed.
    :param seq:
        The last sequence number received.

    :return:
        An OPcode 6 payload in JSON format for reconnecting.
    """

    return {
        'token': token,
        'session_id': session_id,
        'seq': seq
    }
