from ws4py.client.threadedclient import WebSocketClient
import logging
import requests
import json
import gevent
from shitcord.utils.gateway import JSON
from shitcord.gateway.opcodes import Opcodes

log = logging.getLogger(__name__)
url = 'https://discordapp.com/api/v6/gateway/bot'
ws_url = 'wss://gateway.discord.gg/?v=6&encoding=json'


class Start:

    def __init__(self, token):
        self.token = token

        log.debug('Requests: Connecting to {}'.format(url))
        requests.get(url, params={"token": self.token})
        log.debug('Requests: Successfully connected to {}'.format(url))
        DummyClient().connect_ws()


class DummyClient(WebSocketClient):

    def __init__(self):
        super().__init__(ws_url)
        self.message = None
        self.op = None
        self.data = None
        self.seq = None
        self.heart = 41250
        self.event = None

    @staticmethod
    def connect_ws():
        global websocket_client
        websocket_client = DummyClient()
        websocket_client.connect()
        websocket_client.run_forever()

    def opened(self):
        log.debug('WebSocket: Successfully connected!')
        return

    def received_message(self, message):
        self.message = json.loads(str(message))
        self.op = int(self.message.get('op'))
        self.data = self.message.get('d')
        self.seq = self.message.get('s')
        log.info('Received Response:    Sequence number = {}  Opcode = {}'.format(self.seq, self.op))

        if self.op != Opcodes.DISPATCH.value:

            if self.op == Opcodes.RECONNECT.value:
                log.info('Received reconnect opcode.')
                return

            if self.op == Opcodes.HEARTBEAT_ACK.value:
                log.info('Received Heartbeat_ACK opcode.')
                return

            if self.op == Opcodes.HELLO.value:

                try:
                    heart = self.data.get('heartbeat_interval')
                    if heart is not None:
                        self.heart = heart
                except AttributeError:
                    pass

                log.info('Heartbeat: Sending Heartbeat')
                websocket_client.send(JSON.heartbeat())
                log.info('Heartbeat: Successfully send')
                websocket_client.send(JSON.identify())
                gevent.spawn(self.alive_handler()) #It doesn't work
            if self.op == Opcodes.HEARTBEAT:
                websocket_client.send(JSON.heartbeat())
                return

        self.event = self.message.get('t')
        log.info(self.event)

    def alive_handler(self):
        while True:
            log.info('Alive Handler started!')
            gevent.sleep(self.heart / 1000)
            websocket_client.send(JSON.heartbeat(d=self.seq))


Start("TOKEN")
