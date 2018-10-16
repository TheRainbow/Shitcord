import json
import sys


class JSON:

    @staticmethod
    def heartbeat(op=1, d=None):
        payload = {
            'op': op,
            'd': d
        }
        return json.dumps(payload)

    @staticmethod
    def identify(token, game=None):

        data = dict()
        data['op'] = 2
        data['d'] = {}
        data['d']['token'] = token
        data['d']['properties'] = {}
        data['d']['properties']['$os'] = sys.platform
        data['d']['properties']['$browser'] = "Shitcord"
        data['d']['properties']['$device'] = "Shitcord"
        data['d']['compress'] = False
        data['d']['large_threshold'] = 250
        data['d']['shard'] = [0, 1]
        data['d']['presence'] = {}
        data['d']['presence'] = game if game else {"status": "online", "since": 91879201, "afk": False}

        return json.dumps(data)
