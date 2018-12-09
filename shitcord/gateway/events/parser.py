from ..events.error import InvalidEventException
from ..events.event_models import *
from ..events.parsers import ModelParser, NullParser
from ..events.ready import Ready
from shitcord.models import *
from shitcord.models.channel import _channel_from_payload

parsers = dict(
    guild_create=ModelParser(Guild),
    ready=ModelParser(Ready),
    presence_update=ModelParser(PresenceUpdate),
    typing_start=ModelParser(TypingStart),
    message_create=ModelParser(Message),
    message_delete=ModelParser(MessageDelete),
    guild_member_update=ModelParser(GuildMemberUpdate),
    guild_update=ModelParser(Guild),
    message_update=ModelParser(Message),
    message_reaction_add=ModelParser(MessageReaction),
    message_reaction_remove=ModelParser(MessageReaction),
    message_reaction_remove_all=ModelParser(MessageReactionRemoveAll),
    channel_pins_update=ModelParser(ChannelPinsUpdate),
    channel_create=ModelParser(_channel_from_payload),
    channel_update=ModelParser(_channel_from_payload),
    channel_delete=ModelParser(_channel_from_payload),
    guild_ban_add=ModelParser(GuildBan),
    guild_ban_remove=ModelParser(GuildBan),
    guild_member_remove=ModelParser(GuildMemberRemove),
    guild_member_add=ModelParser(GuildMemberAdd),
    guild_member_chunk=ModelParser(GuildMemberChunk),
    guild_role_create=ModelParser(GuildRole),
    guild_role_update=ModelParser(GuildRole),
    guild_role_delete=ModelParser(GuildRoleDelete),
    webhooks_update=ModelParser(WebhooksUpdate),
    voice_state_update=ModelParser(VoiceStateUpdate),
    presences_replace=ModelParser(PresencesReplace)
)


def parse_data(event, data, http):
    if event not in parsers:
        raise InvalidEventException(event)

    return parsers[event].parse(data, http)
