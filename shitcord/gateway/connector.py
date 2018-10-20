import json
import logging

import gevent
from ws4py.client.geventclient import WebSocketClient
from ws4py.messaging import TextMessage

from shitcord.events import parser
from .opcodes import Opcodes
from .serialization import JSON

logger = logging.getLogger(__name__)


class GatewayClient(WebSocketClient):

    def __init__(self, client, gateway, **kwargs):
        self.url = gateway.pop('url')
        self.shards = gateway.pop('shards')
        self._session_start_limit = gateway.pop('session_start_limit')

        super().__init__(self.url, **kwargs)

        self.token = client.api.token
        self.client = client
        self.heart = None
        self.seq = None
        self.connect()
        self.heartbeat_task = gevent.spawn(self.alive_handler)

    @classmethod
    def from_client(cls, client):
        gateway_data = client.api.get_gateway_bot()
        return cls(client, gateway_data, **client.kwargs)

    def join(self):
        self.heartbeat_task.join()

    def opened(self):
        logger.debug('WebSocket: Successfully connected!')

    def alive_handler(self):
        while True:
            if self.seq and self.heart:
                logger.debug('Sending heartbeat.')
                self.send(JSON.heartbeat(d=self.seq))
                gevent.sleep(self.heart / 1000)

    def received_message(self, message: TextMessage):
        message = json.loads(message.data.decode(message.encoding))
        op = Opcodes(message['op'])
        data = message.get('d')
        self.seq = message.get('s')

        if op != Opcodes.DISPATCH:
            logger.debug('Received Response: Sequence number = {}  Opcode = {}'.format(self.seq, op))

            if op == Opcodes.RECONNECT:
                logger.debug('Received reconnect opcode.')

            if op == Opcodes.HEARTBEAT_ACK:
                logger.debug('Received Heartbeat_ACK opcode.')

            if op == Opcodes.HELLO:
                self.heart = data.get('heartbeat_interval')
                self.send(JSON.identify(self.token))

            if op == Opcodes.HEARTBEAT:
                self.send(JSON.heartbeat())
            return

        event = message['t']

        logger.debug('Received Dispatch: event: {}'.format(event, data))
        self.fire_event(event.lower(), data)

    def fire_event(self, name, data):
        data = parser.parse_data(name, data)
        for handler in self.client.events[name]:
            handler(data)
