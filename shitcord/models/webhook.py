from shitcord import *


class WebHook(Model):
    def __init__(self, data):
        super.__init__(data)

        self.id = data['id']
        self.guild_id = data['guild_id']
        self.channel_id = data['channel_id']
        self.name = data['name']
        self.avatar = data['avatar']
        self.token = data['token']
        try:
            self.user = User(data['user'])
        except KeyError:
            self.user = None

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
