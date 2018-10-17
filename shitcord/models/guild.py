from shitcord.models.core import Model
from shitcord.models.emoji import Emoji
from shitcord.models.role import Role


class Guild(Model):
    def __init__(self, data):
        super().__init__(data)
        self.unavailable = data.get('unavailable', False)
        if len(data) == 2:
            return
        self.application_id = data['application_id']
        self.features = data['features']
        self.afk_timeout = int(data['afk_timeout'])
        self.default_message_notifications = int(data['default_message_notifications'])
        self.afk_channel_id = data['afk_channel_id']
        self.explicit_content_filter = int(data['explicit_content_filter'])
        self.id = int(data['id'])
        self.verification_level = int(data['verification_level'])
        self.widget_channel_id = data.get('widget_channel_id')
        self.embed_channel_id = data.get('embed_channel_id')
        self.splash = data['splash']
        self.emojis = [Emoji(emoji) for emoji in data['emojis']]
        self.embed_enabled = data.get('embed_enabled', False)
        self.owner_id = int(data['owner_id'])
        self.mfa_level = int(data['mfa_level'])
        self.embed_enabled = data.get('embed_enabled', False)
        self.system_channel_id = data['system_channel_id']
        self.widget_enabled = data.get('widget_enabled', False)
        self.icon = data['icon']
        self.name = data['name']
        self.roles = [role for role in data['roles']]
        self.region = data['region']

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
