from collections import OrderedDict


class Cache(object):
    def __init__(self, cache_size=5000):
        self._cache_size = cache_size
        self._cache = OrderedDict()

    def resolve(self, key: str, data=None):
        if data:
            self._cache[key] = data
            self.cleanse()

        self._cache.move_to_end(key)
        return self._cache.get(key)

    def cleanse(self):
        if len(self._cache) > self._cache_size:
            self._cache.popitem(last=False)
