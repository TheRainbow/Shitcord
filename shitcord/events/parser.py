from shitcord.events.error import InvalidEventException
from shitcord.events import event_models
from shitcord.events.parsers import ModelParser, NullParser
from shitcord.events.ready import Ready
from shitcord.models import Guild

parsers = dict(
    guild_create=ModelParser(Guild),
    ready=ModelParser(Ready),
    presence_update=ModelParser(event_models.PresenceUpdate),
    typing_start=ModelParser(event_models.TypingStart),
    message_create=NullParser(),
    message_delete=ModelParser(event_models.MessageDelete),
    guild_member_update=NullParser(),
    guild_update=NullParser(),
    message_update=NullParser(),
    message_reaction_add=NullParser(),
    message_reaction_remove=NullParser(),
    message_reaction_remove_all=NullParser(),
    channel_pins_update=NullParser(),
    channel_create=NullParser(),
    channel_update=NullParser(),
    channel_delete=NullParser(),
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
