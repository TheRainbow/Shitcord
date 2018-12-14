# -*- coding: utf-8 -*-

import abc


class Sendable(metaclass=abc.ABCMeta):
    """An Abstract Base Class all models where messages can be sent to must implement.

    This defines some attributes and methods that any model that allows to be the destination
    for sending messages must implement.

    Attributes
    ----------

    Methods
    -------
    """

    __slots__ = ()


class Connectable(metaclass=abc.ABCMeta):
    """An Abstract Base Class all models that allow for connecting must implement.

    These are basically just for VoiceChannels.

    Attributes
    ----------

    Methods
    -------
    """

    __slots__ = ()


class DiscordUser(metaclass=abc.ABCMeta):
    """An Abstract Base Class all models that represent generic Discord Users must implement.

    This basically offers methods that specifically all Discord users like Users and Members
    must implement.

    Attributes
    ----------

    Methods
    -------
    """

    __slots__ = ()


class PrivateChannel(metaclass=abc.ABCMeta):
    """An Abstract Base Class all private channels must implement.

    DM channels as well as DM groups must implement this.

    Attributes
    ----------

    Methods
    -------
    """

    __slots__ = ()


class GuildChannel(metaclass=abc.ABCMeta):
    """An Abstract Base Class all guild channels must implement.

    It provides some general stuff that is necessary for all channels
    from a Guild regardless of the type.

    Attributes
    ----------

    Methods
    -------
    """

    __slots__ = ()
