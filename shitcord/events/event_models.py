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
