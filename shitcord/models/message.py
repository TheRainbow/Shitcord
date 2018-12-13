from ..models.core import Model
from ..models.user import User
from ..models.guild import Guild
from ..models.channel import _channel_from_payload


class Message(Model):
    def __init__(self, data, http):
        super().__init__(data, http)
        self._json = data

        self.response = data
        self.attachments = data['attachments']
        self.tts = data['tts']
        self.embeds = data['embeds']
        self.timestamp = data['timestamp']
        self.mention_everyone = data['mention_everyone']
        self.id = data['id']
        self.pinned = data['pinned']
        self.edited_timestamp = data['edited_timestamp']
        self.author = User(data['author'], http)
        self.mention_roles = data['mention_roles']
        self.content = data['content']
        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.mentions = data['mentions']
        self.type = data['type']
        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http) if data.get('guild_id') else None

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json

    def __repr__(self):
        return '<shitcord.Message id={}, author={}, channel={}, pinned={}>'.format(self.id, self.author, self.channel.id, self.pinned)
