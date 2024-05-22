#!/usr/bin/python3
"""
LRU Cache
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class """

    def __init__(self):
        """Initialize the class """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._move_to_first(key)
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                old_key = self.order.pop(0)
                print("DISCARD: " + old_key)
                del self.cache_data[old_key]
            self.cache_data[key] = item
            self.order.insert(0, key)

    def get(self, key):
        """ Get item from cache """
        if key in self.cache_data:
            self._move_to_first(key)
            return self.cache_data[key]
        return None

    def _move_to_first(self, key):
        """ Move the accessed key to the end """
        if key in self.order:
            self.order.remove(key)
        self.order.insert(0, key)
