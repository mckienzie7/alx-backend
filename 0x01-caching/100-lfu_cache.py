#!/usr/bin/env python3
"""fifo caching method"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    class FIFOCache inherits from BaseCache
    """
    def __init__(self):
        super().__init__()
        self.frequency_cache = {}

    def put(self, key, item):
        """add to cached data"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard_key = min(
                    self.frequency_cache, key=self.frequency_cache.get
                )
                del self.cache_data[discard_key]
                del self.frequency_cache[discard_key]
                print(f"DISCARD: {discard_key}")
            self.cache_data[key] = item
            self.frequency_cache[key] = 1

    def get(self, key):
        """get by key"""
        if key is not None and key in self.cache_data.keys():
            self.frequency_cache[key] += 1
            return self.cache_data.get(key)
        else:
            return None
