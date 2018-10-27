from collections import defaultdict

from shitcord import API
from shitcord import GatewayClient
from shitcord.models.guild import Guild
from shitcord.utils.aliases import default_aliases
from shitcord.utils.cache import Cache


class Client:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.api = None
        self.gateway_client = None
        self._aliases = default_aliases.copy()
        self.events = defaultdict(list)
        self._guilds = {}
        self._message_cache = Cache()

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
        self.gateway_client = GatewayClient.from_client(self)

        self.gateway_client.join()

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
