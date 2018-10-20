from shitcord.models.core import Model


class Channel(Model):
    def __init__(self, data):
        super().__init__(data)

        self.guild_id = data['guild_id']
        self.name = data['name']
        self.permissions_overwrites = data['permission_overwrites']
        self.topic = data['topic']
        self.parent_id = int(data['parent_id'])
        self.nsfw = bool(data['nsfw'])
        self.position = int(data['position'])
        self.rate_limit_per_user = int(data['rate_limit_per_user'])
        self.last_message_id = int(data['last_message_id'])
        self.type = int(data['type'])

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")

    def __repr__(self):
        return '<shitcore.Channel id=%d, name=%r, nsfw=%r, guild=%d>' % (self.id, self.name, self.nsfw, self.guild_id)
