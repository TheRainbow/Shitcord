from shitcord.models.core import Model
from shitcord.models import User


class Webhook(Model):
    def __init__(self, data):
        super().__init__(data)

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
        raise NotImplementedError('Ill do it later. "later"')

    def __repr__(self):
        return '<shitcord.Webhook id=%d, channel=%r, name=%r>' % (self.id, self.channel_id, self.name)
