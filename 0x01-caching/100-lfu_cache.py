#!/usr/bin/python3
from base_caching import BaseCaching
from collections import defaultdict, OrderedDict
"""
LRU Cache with LFU eviction for items with the same frequency
"""


class LFUCache(BaseCaching):
    """ LRUCache class """

    def __init__(self):
        """Initialize the class """
        super().__init__()
        self.order = []
        self.frequency = defaultdict(int)

    def put(self, key, item):
        """ Add item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._move_to_end(key)
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                self._evict()
            self.cache_data[key] = item
            self.order.append(key)
            self.frequency[key] += 1

    def get(self, key):
        """ Get item from cache """
        if key in self.cache_data:
            self._move_to_end(key)
            self.frequency[key] += 1
            return self.cache_data[key]
        return None

    def _move_to_end(self, key):
        """ Move end """
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def _evict(self):
        """ Evict """
        min_freq = min(self.frequency.values())
        least_frequent_keys = [key for key, freq in self.frequency.items() if freq == min_freq]
        lru_key = min(least_frequent_keys, key=lambda k: self.order.index(k))
        print("DISCARD: " + lru_key)
        del self.cache_data[lru_key]
        self.order.remove(lru_key)
        del self.frequency[lru_key]
