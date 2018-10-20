from datetime import datetime

from shitcord.models.core import Model, Snowflake


class TypingStart(Model):

    def __init__(self, data):
        super().__init__({'id': Snowflake.create_snowflake(datetime.fromtimestamp(data['timestamp']))})
        self.channel = data['channel_id']
        self.guild = data.get('guild_id')
        self.user = data['user_id']

    def to_json(self):
        pass


class PresenceUpdate(Model):

    def __init__(self, data):
        super().__init__({'id': 0})
        self.activities = data['activities']
        self.game = data['game']
        self.guild = data.get('guild_id')
        self.nick = data['nick']
        self.roles = data.get('roles')
        self.status = data['status']
        self.user = data['user']

    def to_json(self):
        pass


class MessageDelete(Model):

    def __init__(self, data):
        super().__init__({'id': 0})
        self.id = data['id']
        self.channel = data['channel_id']
        self.guild = data['guild_id']

    def to_json(self):
        pass
