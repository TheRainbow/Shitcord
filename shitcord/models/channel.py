import enum
from datetime import datetime

from .core import Model

__all__ = ['TextChannel', 'DMChannel', 'VoiceChannel', 'GroupDMChannel', 'CategoryChannel', '_channel_from_payload']


def _channel_from_payload(data, http):
    channel_type = IntChannelTypes(data['type']).name
    channel_cls = ChannelTypes[channel_type]

    return channel_cls(data, http)


def _get_as_datetime(data, key):
    item = data.get(key)
    if not item:
        return None

    return datetime.utcfromtimestamp(item)


class BaseChannel(Model):
    def __init__(self, data, http):
        self._json = data
        super().__init__(data['id'], http)

        self.type = data['type']

    def __repr__(self):
        raise NotImplementedError

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class PartialChannel(BaseChannel):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['name']

    def __repr__(self):
        return '<shitcord.PartialChannel id={} name={}>'.format(self.id, self.name)


class TextChannel(BaseChannel):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.guild_id = data['guild_id']
        self.position = data['position']
        self.permission_overwrites = data['permission_overwrites']
        self.name = data['name']
        self.topic = data.get('topic', '')
        self.nsfw = data['nsfw']
        self.last_message_id = data.get('last_message_id')
        self.rate_limit = data.get('rate_limit_per_user', 0)
        self.parent_id = data.get('parent_id')
        self.last_pinned = _get_as_datetime(data, 'last_pin_timestamp')

    def __repr__(self):
        return '<shitcord.TextChannel id={} name={} guild_id={} nsfw={}>'.format(self.id, self.name, self.guild_id, self.nsfw)


class DMChannel(BaseChannel):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.last_message_id = data.get('last_message_id')
        self.recipients = data['recipients']
        self.last_pinned = _get_as_datetime(data, 'last_pin_timestamp')

    def __repr__(self):
        return '<shitcord.DMChannel id={}>'.format(self.id)


class VoiceChannel(BaseChannel):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.guild_id = data['guild_id']
        self.position = data['position']
        self.permission_overwrites = data['permission_overwrites']
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        self.parent_id = data.get('parent_id')

    def __repr__(self):
        return '<shitcord.VoiceChannel id={} name={} bitrate={} user_limit={}>'.format(self.id, self.name, self.bitrate, self.user_limit)


class GroupDMChannel(BaseChannel):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['name']
        self.last_message_id = data.get('last_message_id')
        self.recipients = data['recipients']
        self.icon = data.get('icon')
        self.owner_id = data['owner_id']
        self.application_id = data.get('application_id')
        self.last_pinned = _get_as_datetime(data, 'last_pin_timestamp')

    def __repr__(self):
        return '<shitcord.GroupDMChannel id={} name={} owner_id={}>'.format(self.id, self.name, self.owner_id)


class CategoryChannel(BaseChannel):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.guild_id = data['guild_id']
        self.position = data['position']
        self.permission_overwrites = data['permission_overwrites']
        self.name = data['name']
        self.nsfw = data['nsfw']
        self.parent_id = data.get('parent_id')

    def __repr__(self):
        return '<shitcord.CategoryChannel id={} name={} guild_id={} nsfw={}>'.format(self.id, self.name, self.guild_id, self.nsfw)


class IntChannelTypes(enum.IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4


class ChannelTypes(enum.Enum):
    GUILD_TEXT = TextChannel
    DM = DMChannel
    GUILD_VOICE = VoiceChannel
    GROUP_DM = GroupDMChannel
    GUILD_CATEGORY = CategoryChannel
