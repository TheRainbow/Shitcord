import json
import logging

import gevent
from ws4py.client.threadedclient import WebSocketClient
from ws4py.messaging import TextMessage

from .opcodes import Opcodes
from .serialization import JSON

log = logging.getLogger(__name__)
url = 'https://discordapp.com/api/v6/gateway/bot'
ws_url = 'wss://gateway.discord.gg/?v=6&encoding=json'


class GatewayClient(WebSocketClient):

    def __init__(self, token):
        super(GatewayClient, self).__init__(ws_url)
        self.token = token
        self.heart = None
        self.seq = None
        self.connect()
        self.greenlet = gevent.spawn(self.alive_handler)

    def join(self):
        self.greenlet.join()

    def opened(self):
        log.debug('WebSocket: Successfully connected!')

    def alive_handler(self):
        while True:
            if self.seq and self.heart:
                log.debug('Sending heartbeat.')
                self.send(JSON.heartbeat(d=self.seq))
                gevent.sleep(self.heart / 1000)

    def received_message(self, message: TextMessage):
        message = json.loads(message.data.decode(message.encoding))
        op = Opcodes(message['op'])
        data = message.get('d')
        self.seq = self.seq or message['s']

        if op != Opcodes.DISPATCH:
            log.info('Received Response: Sequence number = {}  Opcode = {}'.format(self.seq, op))
            if op == Opcodes.RECONNECT:
                log.info('Received reconnect opcode.')

            if op == Opcodes.HEARTBEAT_ACK:
                log.info('Received Heartbeat_ACK opcode.')

            if op == Opcodes.HELLO:
                self.heart = self.heart or data['heartbeat_interval']
                self.send(JSON.identify(self.token))

            if op == Opcodes.HEARTBEAT:
                self.send(JSON.heartbeat())
            return

        event = message['t']

        log.debug('Received Dispatch: event: {}'.format(event, data))
