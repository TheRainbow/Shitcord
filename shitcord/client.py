from collections import defaultdict

from shitcord import API
from shitcord import GatewayClient
from shitcord.utils.aliases import default_aliases


class Client:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.api = None
        self.gateway_client = None
        self._aliases = default_aliases.copy()
        self.events = defaultdict(list)

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

    def _resolve_alias(self, event):
        return self._aliases.get(event, event)

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
