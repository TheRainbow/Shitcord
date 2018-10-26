import json
import logging
from datetime import datetime

import gevent
from ws4py.client.geventclient import WebSocketClient
from ws4py.messaging import TextMessage

from shitcord.events import parser
from shitcord.gateway.caching import store
from shitcord.gateway.opcodes import Opcodes
from shitcord.gateway.serialization import JSON

logger = logging.getLogger(__name__)
none_function = lambda *args, **kwargas: None


class GatewayClient(WebSocketClient):

    def __init__(self, client, gateway, **kwargs):
        self.url = gateway.pop('url')
        self.shards = gateway.pop('shards')
        self._session_start_limit = gateway.pop('session_start_limit')

        super().__init__(self.url, **kwargs)

        self.token = client.api.token
        self.client = client
        self.heart = None
        self.sessid = None
        self.seq = None
        self.latest_ack = None
        self.latest_heart = None
        self.connect()
        self.heartbeat_task = gevent.spawn(self.alive_handler)

    @classmethod
    def from_client(cls, client):
        gateway_data = client.api.get_gateway_bot()
        return cls(client, gateway_data, **client.kwargs)

    def join(self):
        self.heartbeat_task.join()

    def opened(self):
        if self.sessid:
            self.send(JSON.resume(self.token, self.sessid, self.seq))
            logger.debug('WebSocket: Successfully connected!')

    def alive_handler(self):
        logging.debug('Activated Alive Handler!')
        while True:
            if self.seq and self.heart:
                if self.latest_ack and self.latest_heart and self.latest_ack < self.latest_heart:
                    raise RuntimeError("TIMEOUT")
                logger.debug('Sending heartbeat.')
                self.latest_heart = datetime.now()
                self.send(JSON.heartbeat(d=self.seq))
                gevent.sleep(self.heart / 1000)
            else:
                gevent.sleep(0)

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
                self.latest_ack = datetime.now()

            if op == Opcodes.HELLO:
                self.heart = data.get('heartbeat_interval')
                self.send(JSON.identify(self.token))

            return

        event = message['t']

        logger.debug('Received Dispatch: event: {}'.format(event, data))
        self.fire_event(event.lower(), data)

    def fire_event(self, name, data):
        if name == 'ready':
            self.sessid = data['session_id']

        data = parser.parse_data(name, data)

        store(self.client, data)

        for handler in self.client.events[name]:
            handler(data)

        # noinspection PyProtectedMember
        for alias in [key for key, value in self.client._aliases.items() if value == name] + [name]:
            getattr(self.client, 'on_' + alias, none_function)(data)
