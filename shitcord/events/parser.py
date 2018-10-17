from shitcord.events.error import InvalidEventException
from shitcord.events.event_models import TypingStart, PresenceUpdate
from shitcord.events.parsers import ModelParser, NullParser
from shitcord.events.ready import Ready
from shitcord.models import Guild

parsers = dict(
    guild_create=ModelParser(Guild),
    ready=ModelParser(Ready),
    presence_update=ModelParser(PresenceUpdate),
    typing_start=ModelParser(TypingStart),
    message_create=NullParser(),
    message_delete=NullParser(),
    guild_member_update=NullParser(),
    guild_update=NullParser(),
    message_update=NullParser()
)


def parse_data(event, data):
    if event not in parsers:
        raise InvalidEventException(event)
    return parsers[event].parse(data)
