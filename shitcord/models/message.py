from shitcord.models.core import Model


class Message(Model):
    def __init__(self, data):
        super().__init__(data)

        self.response = data
        self.attachments = data['attachments']
        self.tts = bool(data['tts'])
        self.embeds = data['embeds']
        self.timestamp = data['timestamp']
        self.mention_everyone = bool(data['mention_everyone'])
        self.id = int(data['id'])
        self.pinned = bool(data['pinned'])
        self.edited_timestamp = data['edited_timestamp']
        self.author = User(data['author'])
        self.mention_roles = data['mention_roles']
        self.content = data['content']
        self.channel_id = data['channel_id']
        self.mentions = data['mentions']
        self.type = int(data['type'])

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
