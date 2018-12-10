# -*- coding: utf-8 -*-

from collections import OrderedDict


class Cache:
    """Represents a generic cache for models from the Discord API.

    Parameters
    ----------
    cache_size : int, optional
        The total amount of items that can be in the cache at the same time. Defaults to 5000.
    """

    def __init__(self, *, cache_size=5000):
        self._cache_size = cache_size
        self._cache = OrderedDict()

    def resolve(self, key, data=None):
        """Resolves a key from the cache.

        Parameters
        ----------
        key : str
            The key to retrieve the corresponding value from the cache.
        data : optional
            An optional value to add to the cache for further retrieval using the specified key.
        """

        if data:
            self._cache[key] = data
            self._cleanse()

        self._cache.move_to_end(key)
        return self._cache.get(key)

    def _cleanse(self):
        if len(self._cache) > self._cache_size:
            self._cache.popitem(last=False)
