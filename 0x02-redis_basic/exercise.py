#!/usr/bin/env python3
"""
Cache module with a Cache class that utilizes Redis for data storage.
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method of the Cache class is called.

    :param method: The method to be decorated.
    :return: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}_calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


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

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        :param data: The data to be stored.
        :return: The randomly generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key.

        key: The key used for retrieving data from Redis.
        fn: Optional callable to convert the data back to the desired format.
        return: The retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string from Redis using the provided key.

        key: The key used for retrieving the string from Redis.
        return: The retrieved string or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer from Redis using the provided key.

        :param key: The key used for retrieving the integer from Redis.
        :return: The retrieved integer or None if the key does not exist.
        """
        return self.get(key, fn=int)
