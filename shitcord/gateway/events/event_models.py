from datetime import datetime

from shitcord.models.core import Model, Snowflake
from shitcord.models.channel import _channel_from_payload
from shitcord.models.guild import Guild
from shitcord.models.user import User
from shitcord.models.message import Message
from shitcord.models.emoji import Emoji
from shitcord.models.role import Role


__all__ = ['TypingStart', 'PresenceUpdate', 'MessageDelete', 'ChannelPinsUpdate', 'GuildMemberUpdate',
           'MessageReaction', 'MessageReactionRemoveAll', 'GuildBan', 'GuildMemberRemove', 'GuildMemberAdd',
           'GuildMemberChunk', 'GuildRole', 'GuildRoleDelete', 'WebhooksUpdate', 'VoiceStateUpdate', 'PresencesReplace']


class TypingStart(Model):

    def __init__(self, data, http):

        super().__init__(Snowflake.create_snowflake(datetime.fromtimestamp(data['timestamp'])), http)
        self._json = data

        self.channel = data['channel_id']
        self.guild = data.get('guild_id')
        self.user_id = data['user_id']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class PresenceUpdate(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.activities = data['activities']
        self.game = data['game']
        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.nick = data.get('nick', None)
        self.roles = data.get('roles')
        self.status = data['status']
        self.user = data['user']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class MessageDelete(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.id = data['id']
        self.channel = self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.guild_id = data.get('guild_id')

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class ChannelPinsUpdate(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.last_pin_timestamp = data.get('last_pin_timestamp')

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildMemberUpdate(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.roles = [role for role in data['roles']]
        self.user = User(data['user'], self._http)
        self.nick = data['nick']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class MessageReaction(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = data.get('guild_id')
        self.user = User(self._http.get_user(data['user_id']), self._http)
        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.message = Message(self._http.get_channel_message(self.channel.id, data['message_id']), self._http)
        self.emoji = Emoji(data['emoji'], self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class MessageReactionRemoveAll(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = data.get('guild_id')
        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)
        self.message = Message(self._http.get_channel_message(self.channel.id, data['message_id']), self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildBan(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.user = User(data['user'], self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildMemberAdd(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildMemberRemove(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.user = User(data['user'], self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildMemberChunk(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.users = [User(user, self._http) for user in data['members']]

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildRole(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.role = Role(data['role'], self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class GuildRoleDelete(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.role_id = data['role']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class WebhooksUpdate(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

        self.guild = Guild(self._http.get_guild(data['guild_id']), self._http)
        self.channel = _channel_from_payload(self._http.get_channel(data['channel_id']), self._http)

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class VoiceStateUpdate(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data
        self.token = data['token']
        self.guild = Guild(self._http.get_guild(data['guild_id'], self._http))
        self.endpoint = data['endpoint']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)
        return json


class PresencesReplace(Model):

    def __init__(self, data, http):
        super().__init__(0, http)
        self._json = data

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)
        return json
