from ..models.core import Model
from ..models import User
from ..models.channel import _channel_from_payload


class Webhook(Model):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.id = data['id']
        self.guild_id = data['guild_id']
        self.channel_id = data['channel_id']
        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.name = data['name']
        self.avatar = data['avatar']
        self.token = data['token']
        try:
            self.user = User(data['user'], http)
        except KeyError:
            self.user = None

    def to_json(self):
        raise NotImplementedError('Ill do it later. "later"')

    def __repr__(self):
        return '<shitcord.Webhook id={}, channel={}, name={}>'.format(self.id, self.channel_id, self.name)
