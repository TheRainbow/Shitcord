from ..models.core import Model
from ..models.user import User
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
        self.channel_id = data['channel_id']
        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.mentions = data['mentions']
        self.type = data['type']

    def to_json(self):
        raise NotImplementedError('Ill do it later. "later"')

    def __repr__(self):
        return '<shitcord.Message id=%d, author=%r, channel=%r, pinned=%r>' % (self.id, self.author, self.channel_id, self.pinned)
