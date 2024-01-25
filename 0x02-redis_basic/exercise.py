#!/usr/bin/env python3
"""
Cache module with a Cache class that utilizes Redis for data storage.
"""
import redis
import uuid
from typing import Union

#redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class Cache:
    """
    Cache class that uses Redis for data storage.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance with a Redis client.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        :param data: The data to be stored.
        :return: The randomly generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
