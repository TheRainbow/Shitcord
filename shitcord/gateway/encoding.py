# -*- coding: utf-8 -*-

import abc

import erlastic

try:
    import ujson as json
except ImportError:
    import json


class BaseEncoder(abc.ABC):
    """
    An Abstract Base Class for implementing encoders to communicate with the Discord Gateway.
    """

    TYPE = None
    IS_BINARY = None

    @staticmethod
    @abc.abstractmethod
    def decode(data):
        pass

    @staticmethod
    @abc.abstractmethod
    def encode(data):
        pass


class ETFEncoder(BaseEncoder):
    """
    An encoder that will be used to handle received Gateway payloads.

    This will be used when communication should be done in Erlang's ETF format.
    """

    TYPE = 'etf'
    IS_BINARY = True

    @staticmethod
    def decode(data):
        return erlastic.decode(data)

    @staticmethod
    def encode(data, *, compressed=True):
        return erlastic.encode(data, compressed)


class JSONEncoder(BaseEncoder):
    """
    An encoder that will be used to handle received Gateway payloads.

    This will be used when communication should be done in JSON format.
    """

    TYPE = 'json'
    IS_BINARY = False

    @staticmethod
    def decode(data):
        return json.loads(data)

    @staticmethod
    def encode(data):
        return json.dumps(data)


# We will use this dict later on to retrieve the needed encoder for the chosen payload compression.
encoders = {
    'json': JSONEncoder,
    'etf': ETFEncoder
}
