from ..events.error import InvalidEventException
from ..events.event_models import *
from ..events.parsers import ModelParser, NullParser
from ..events.ready import Ready
from ..models import *

parsers = dict(
    guild_create=ModelParser(Guild),
    ready=ModelParser(Ready),
    presence_update=ModelParser(PresenceUpdate),
    typing_start=ModelParser(TypingStart),
    message_create=ModelParser(Message),
    message_delete=ModelParser(MessageDelete),
    guild_member_update=NullParser(),
    guild_update=NullParser(),
    message_update=ModelParser(Message),
    message_reaction_add=NullParser(),
    message_reaction_remove=NullParser(),
    message_reaction_remove_all=NullParser(),
    channel_pins_update=ModelParser(ChannelPinsUpdate),
    channel_create=ModelParser(TextChannel),
    channel_update=ModelParser(TextChannel),
    channel_delete=ModelParser(TextChannel),
    guild_ban_add=NullParser(),
    guild_ban_remove=NullParser(),
    guild_member_remove=NullParser(),
    guild_member_add=NullParser(),
    guild_member_chunk=NullParser(),
    guild_role_create=NullParser(),
    guild_role_update=NullParser(),
    guild_role_delete=NullParser(),
    webhooks_update=NullParser(),
    voice_state_update=NullParser(),
    presences_replace=NullParser()
)


def parse_data(event, data, http):
    if event not in parsers:
        raise InvalidEventException(event)

    return parsers[event].parse(data, http)
