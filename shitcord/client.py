import time
from collections import defaultdict

from . import Activity, API, DiscordWebSocketClient, Guild, Opcodes, StatusType, utils


class Client:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.api = None
        self.ws = None
        self._aliases = utils.aliases.default_aliases.copy()
        self.events = defaultdict(list)
        self._guilds = {}
        self._message_cache = utils.cache.Cache()

    def _resolve_alias(self, event):
        return self._aliases.get(event, event)

    def _store_guild(self, guild: Guild):
        self._guilds[guild.id] = guild

    # Public API

    def start(self, token: str):
        """
        Connects the Client to the API and the Gateway and makes
        interaction with both elements possible.

        :param token:
            The bot's token
        """

        self.api = API(token)
        self.ws = DiscordWebSocketClient.from_client(self)
        self.ws.run_forever()

    def change_presence(self, *, activity: Activity = None, status: StatusType = StatusType.ONLINE, afk=False, since=0.0):
        """
        Changes a bot's presence.
        This sets a 'Playing ...'/'Listening to ...', whatever status visible in the
        Discord client.

        :param activity:
            An `Activity` object containing all necessary information about the game.
        :param status:
            A valid `StatusType` denoting the bot's "action". E.g. playing, listening, streaming, watching...
        :param afk:
            Whether or not the bot should show up as afk.
        :param since:
            The given interval since when the bot started being afk.
        """

        if not isinstance(activity, Activity):
            raise TypeError('Activity must be an Activity model.')

        if status is StatusType.IDLE and not since:
            since = int(time.time() * 1000)

        payload = {
            'since': since,
            'game': None,
            'status': status.name.lower(),
            'afk': afk,
        }

        if activity:
            payload['game'] = activity.to_json()

        return self.ws.send(Opcodes.STATUS_UPDATE, payload)

    def on(self, event: str):
        """
        Registers a new event for the Client.

        :param event:
            A string that represents the type of the event.
        """

        def decorator(func):
            self.events[self._resolve_alias(event)].append(func)
            return func

        return decorator

    def get_guild(self, id) -> Guild:
        return self._guilds.get(id)
