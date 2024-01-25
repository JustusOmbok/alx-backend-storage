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
    key = f"{method.__name__}_calls"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.

    :param method: The method to be decorated.
    :return: The decorated method.
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Store input arguments
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(outputs_key, output)

        return output

    return wrapper

def replay(func: Callable) -> None:
    """
    Display the history of calls of a particular function.

    :param func: The function whose history is to be displayed.
    """
    inputs_key = f"{func.__qualname__}:inputs"
    outputs_key = f"{func.__qualname__}:outputs"

    inputs = [eval(arg) for arg in cache._redis.lrange(inputs_key, 0, -1)]
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{func.__qualname__}(*{args}) -> {output.decode('utf-8')}")

class Cache:
    """
    Cache class that uses Redis for data storage.
    """

    _redis = redis.Redis()

    def __init__(self) -> None:
        """
        Initialize the Cache instance with a Redis client and flush the Redis database.
        """
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        :param data: The data to be stored, which can be str, bytes, int, or float.
        :return: The randomly generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @count_calls
    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key.

        :param key: The key used for retrieving data from Redis.
        :param fn: Optional callable to convert the data back to the desired format.
        :return: The retrieved data, possibly converted using the provided callable.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string from Redis using the provided key.

        :param key: The key used for retrieving the string from Redis.
        :return: The retrieved string or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer from Redis using the provided key.

        :param key: The key used for retrieving the integer from Redis.
        :return: The retrieved integer or None if the key does not exist.
        """
        return self.get(key, fn=int)
