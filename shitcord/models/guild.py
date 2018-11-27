from ..models.core import Model
from ..models.emoji import Emoji
from ..models.user import User


class Guild(Model):
    def __init__(self, data, http):
        super().__init__(data, http)
        self._json = data

        self.unavailable = data.get('unavailable')
        self.application_id = data['application_id']
        self.features = data['features']
        self.afk_timeout = data['afk_timeout']
        self.default_message_notifications = data['default_message_notifications']
        self.afk_channel_id = data['afk_channel_id']
        self.explicit_content_filter = data['explicit_content_filter']
        self.id = data.get('id', 0)
        self.verification_level = data['verification_level']
        self.widget_channel_id = data.get('widget_channel_id')
        self.embed_channel_id = data.get('embed_channel_id')
        self.splash = data['splash']
        self.emojis = [Emoji(emoji, http) for emoji in data['emojis']]
        self.embed_enabled = data.get('embed_enabled')
        self.owner_id = data['owner_id']
        self.owner = User(self._http.get_user(self.owner_id), http)
        self.mfa_level = data['mfa_level']
        self.system_channel_id = data['system_channel_id']
        self.widget_enabled = data.get('widget_enabled')
        self.icon = data['icon']
        self.name = data['name']
        self.roles = [role for role in data['roles']]
        self.region = data['region']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json

    def __repr__(self):
        return '<shitcore.Guild id={}, name={}>'.format(self.id, self.name)
