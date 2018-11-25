from datetime import datetime

from shitcord.models.core import Model, Snowflake

__all__ = ['TypingStart', 'PresenceUpdate', 'MessageDelete']


class TypingStart(Model):

    def __init__(self, data, http):

        super().__init__(Snowflake.create_snowflake(datetime.fromtimestamp(data['timestamp'])), http)
        self.channel = data['channel_id']
        try:
            self.guild = data['guild_id']
        except KeyError:
            pass
        self.user_id = data['user_id']

    def to_json(self):
        pass


class PresenceUpdate(Model):

    def __init__(self, data, http):
        super().__init__(0, http)

        self.activities = data['activities']
        self.game = data['game']
        self.guild = data.get('guild_id')
        self.nick = data.get('nick', None)
        self.roles = data.get('roles')
        self.status = data['status']
        self.user = data['user']

    def to_json(self):
        pass


class MessageDelete(Model):

    def __init__(self, data, http):
        super().__init__(0, http)

        self.id = data['id']
        self.channel = data['channel_id']
        self.guild = data['guild_id']

    def to_json(self):
        pass
