# -*- coding: utf-8 -*-

import shitcord

import logging
import zlib

import gevent
from eventemitter import EventEmitter
from ws4py.client.geventclient import WebSocketClient

from .caching import store
from .encoding import encoders
from .errors import GatewayException
from .opcodes import Opcodes
from .serialization import identify, resume
from ..utils import gateway
from .events.parser import parse_data

logger = logging.getLogger(__name__)

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
none_func = lambda *a, **kw: None


class DiscordWebSocketClient(WebSocketClient):
    VERSION = 6

    def __init__(self, *gateway_data, max_reconnects=5, encoder='json', zlib_compressed=True, **kwargs):
        """
        Represents the WebSocket Client that will be used to connect to the Discord Gateway v6.
        This will be created by using the `from_client` method. As a library user, you should never create this manually

        :param gateway_data:
            The data required for connecting to the Discord Gateway received from the `get_gateway_bot` method.
        :param max_reconnects:
            The amount of retries to connect to the Discord Gateway after failing.
            Defaults to 5.
        :param encoder:
            The encoder that should be used. Either `json` or `etf`.
        :param zlib_compressed:
            Whether the Discord Gateway should send zlib-Compressed streams.
        :param kwargs:
            Some additional arguments that can be passed.
        """

        # Necessary attributes for determining encoding and compression of payloads
        self.max_reconnects = max_reconnects
        self.encoder = encoders.get(encoder)
        self.zlib_compressed = zlib_compressed

        # Necessary Gateway data
        url, shard, session_limit = gateway_data
        self._gateway_url = self.format_url(url)
        self.shard_id, self.shard_count = 0, shard  # Currently only support for one shard.
        self._session_start_limit = gateway.SessionStartLimit.from_payload(session_limit)
        del url, shard, session_limit

        # Now after gathering all necessary attributes, we can finally initialize the parent class.
        super().__init__(self._gateway_url, **kwargs)

        # For connection state
        self.session_id = None
        self.sequence = 0
        self.reconnects = 0
        self.shutting_down = False

        # Heartbeating stuff
        self.interval = None
        self._heartbeat_ack = True
        self._heartbeat_task = gevent.spawn(self.__alive_handler)

        # Necessary for rate limit handling. It's actually 60, 120, but let's give us some buffer
        self.limiter = gateway.Limiter(2, 1)

        # Necessary for detecting zlib-compressed payloads
        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()

        # For emitting received opcodes
        self.emitter = EventEmitter()

        self.emitter.on('DISPATCH', self._handle_dispatch)
        self.emitter.on('HEARTBEAT', self._handle_heartbeat)
        self.emitter.on('RECONNECT', self._handle_reconnect)
        self.emitter.on('INVALID_SESSION', self._handle_invalid_session)
        self.emitter.on('HELLO', self._handle_hello)
        self.emitter.on('HEARTBEAT_ACK', self._handle_heartbeat_ack)

    @classmethod
    def from_client(cls, client, max_reconnects=5, encoder='json', zlib_compressed=True, **kwargs):
        """
        Initializes a new Gateway client from a given API client.
        This is for internal purposes only.
        Always use this for initializing a new Gateway client.

        :param client:
            The API client.
        :param max_reconnects:
            The total amount of reconnects allowed.
        :param encoder:
            The encoding for payloads that should be used.
        :param zlib_compressed:
            Whether the Gateway should send zlib-compressed streams or not.
        :param kwargs:
            Some additional arguments that should be used.

        :return:
            A new instance of `DiscordWebSocketClient`.
        """
        cls.client = client
        gateway_data = client.api.get_gateway_bot()

        return cls(*gateway_data, max_reconnects=max_reconnects, encoder=encoder, zlib_compressed=zlib_compressed, **kwargs)

    def format_url(self, url):
        """
        Formats the WebSocket URL for connecting to the Discord Gateway.

        :param url:
            The WebSocket URL received from the `Get Gateway Bot` endpoint.

        :return:
            The final WebSocket URL that should be used for connecting to the Gateway.
        """

        url += '?version={}&encoding={}'
        if self.zlib_compressed:
            url += '&encoding=zlib-stream'

        return url.format(self.VERSION, self.encoder.TYPE)

    def _send(self, opcode, payload):
        logger.debug('Sending %s', payload)
        super().send(self.encoder.encode({
            'op': opcode.value,
            'd': payload,
        }), self.encoder.IS_BINARY)

    def send(self, opcode, payload):
        self.limiter.check()
        self._send(opcode, payload)

    def __alive_handler(self):
        while True:
            if not self._heartbeat_ack:
                logger.warning('No HEARTBEAT_ACK received from that shit. Forcing a reconnect.')
                self._heartbeat_ack = True
                self.close(4000, 'Zombied connection, you shitters.')

            if self.sequence:
                logger.debug('Sending Heartbeat with Sequence: %s', self.sequence)
                self._send(Opcodes.HEARTBEAT, self.sequence)
                self._heartbeat_ack = False
                gevent.sleep(self.interval / 1000)

            else:
                gevent.sleep(0)

    def _handle_dispatch(self, name, payload):
        if name == 'ready':
            self.session_id = payload['session_id']

        data = parse_data(name, payload, self.client.api)  # TODO: Make this crap not take an API instance as parameter.
        store(self.client, data)

        for handler in self.client.events[name]:
            gevent.spawn(handler, data)

        for alias in [key for key, value in self.client._aliases.items() if value == name] + [name]:
            handler = getattr(self.client, 'on_' + alias, none_func)
            gevent.spawn(handler, data)

    def _handle_heartbeat(self, _):
        logger.debug('Heartbeat requested by the Discord Gateway.')
        self._send(Opcodes.HEARTBEAT, self.sequence)

    def _handle_reconnect(self, _):
        logger.debug('Received Opcode 7: RECONNECT. Forcing a fresh reconnect.')
        self.session_id = None
        self.reconnects = 0
        self.close(reason='Received RECONNECT request.')

    def _handle_invalid_session(self, _):
        logger.debug('Received Opcode 9: INVALID_SESSION. Forcing a fresh reconnect.')
        self.session_id = None
        self.reconnects = 0
        self.close(reason='The current session was invalidated.')

    def _handle_hello(self, payload):
        logger.debug('Received Opcode 10: HELLO. Starting to perform the heartbeat task.')
        self.interval = payload['heartbeat_interval']

    def _handle_heartbeat_ack(self, _):
        logger.debug('Received HEARTBEAT_ACK.')
        self._heartbeat_ack = True

    def opened(self):
        if self.sequence and self.session_id:
            # As of these attributes being set, we try to resume the connection.
            logger.debug('WebSocket connection established: Trying to resume with Session ID: %s and Sequence: %s', self.session_id, self.sequence)
            self._send(Opcodes.RESUME, resume(self.client.api.token, self.session_id, self.sequence))

        else:
            logger.debug('WebSocket connection established: Sending Identify payload.')
            shard = [self.shard_id, self.shard_count]  # Currently only support for one shard.
            self._send(Opcodes.IDENTIFY, identify(self.client.api.token, shitcord.__title__, shard=shard))

    def received_message(self, message):
        msg = message.data
        logger.debug('Received message: %s', msg)

        # First of all, detect zlib-compressed payloads and decompress them.
        if self.zlib_compressed:
            if message.is_binary:
                self._buffer.extend(msg)

                if len(msg) < 4 or msg[-4:] != ZLIB_SUFFIX:
                    return

                msg = self._inflator.decompress(self._buffer)
                # If our encoder isn't binary-based, decode the message as utf-8.
                if not self.encoder.IS_BINARY:
                    msg = msg.decode('utf-8')
                    print(msg)

                # And reset our buffer after the stored data were retrieved.
                self._buffer = bytearray()

        else:
            # As there are special cases where zlib-compressed payloads also occur, even
            # if zlib-stream wasn't specified in the Gateway url, also try to detect them.
            is_json = msg[0] == '{'
            is_etf = msg[0] == 131
            if not is_json and not is_etf:
                try:
                    msg = zlib.decompress(msg, 15, 10490000).decode('utf-8')
                except zlib.error:
                    # If the message cannot be decompressed by zlib, it's a normal utf-8 message
                    msg = msg.decode('utf-8')

        logger.debug('After being decompressed: %s', msg)

        # Now decode the format of the payloads that was specified in the url for connecting.
        try:
            payload = self.encoder.decode(msg)
        except Exception:
            logger.debug('Failed to parse Gateway message %s', msg)
            return

        logger.debug('After being decoded: %s', payload)

        # And now we update the sequence required for heartbeating and resumes.
        if payload['s'] and payload['s'] > self.sequence:
            self.sequence = payload['s']

        # And finally handle the payload's actual content and emit the event corresponding to the opcode.
        opcode = Opcodes(payload['op'])
        data = payload['d']

        if opcode is Opcodes.DISPATCH:
            # For the special case of an event dispatch.
            event = payload['t']
            logger.debug('Received event dispatch %s', event)

            self.emitter.emit(opcode.name, event.lower(), data)
            return

        self.emitter.emit(opcode.name, data)

    def unhandled_error(self, error):
        raise GatewayException('An error occurred: {}'.format(error))

    def closed(self, code, reason=None):
        # Clean up any old data
        self._buffer = bytearray()
        self._heartbeat_task.kill()

        # If we're doing a manual shutdown, there's no need to reconnect.
        if self.shutting_down:
            self.close_connection()
            return

        # Tracking the reconnects
        self.reconnects += 1
        if self.reconnects >= self.max_reconnects:
            raise GatewayException('Total amount of allowed reconnects was exceeded. Shutting down.')

        # Make sure to not resume when the connection was closed with status code between 4000 and 4011.
        # This is usually the case when a connection was sending heartbeats but didn't receive HEARTBEAT_ACKs.
        if code and 4000 <= code <= 4011:
            self.interval = None
            self.session_id = None

            # Inform people about sharding-related errors.
            if code == 4011:
                logger.critical('Unable to connect to the Gateway because this bot requires sharding which is not implemented yet.')

        action = 'resume' if self.session_id else 'reconnect'
        delay = self.reconnects + 10.
        logger.debug('Connection was closed. Attempt to %s in %s seconds.', action, delay)
        gevent.sleep(delay)

        self.connect()

    def destroy(self):
        logger.debug('Shutting down the Gateway client.')
        self.shutting_down = True
        self.close(reason='The connection was manually terminated.')

    def run_forever(self):
        logger.debug('Connecting to the Discord Gateway...')
        gevent.spawn(self.connect)
        self._heartbeat_task.join()
