from shitcord.events.error import InvalidEventException
from shitcord.events.event_models import TypingStart
from shitcord.events.parsers import ModelParser, NullParser
from shitcord.events.ready import Ready
from shitcord.models import Guild

parsers = dict(
    guild_create=ModelParser(Guild),
    ready=ModelParser(Ready),
    presence_update=NullParser(),
    typing_start=ModelParser(TypingStart),
)


def parse_data(event, data):
    if event not in parsers:
        raise InvalidEventException(event)
    return parsers[event].parse(data)
