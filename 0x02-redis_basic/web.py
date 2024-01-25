#!/usr/bin/env python3
""" Module for task 5.
"""

import requests
import redis
import time
from functools import wraps
from typing import Callable, Any, Union


def count_accesses(method: Callable) -> Callable:
    """
    Decorator to track the number of accesses made to a particular URL.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs) -> str:
        """
        Increments the access count for the given URL and invokes the decorated method.

        Args:
            url (str): The URL being accessed.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            str: The result of the decorated method.
        """
        count_key = f"count:{url}"
        method._redis.incr(count_key)
        return method(url, *args, **kwargs)
    return wrapper

def cache_result(expiration_time: int) -> Callable:
    """
    Decorator to cache the result of a method with a specified expiration time.

    Args:
        expiration_time (int): The expiration time for caching in seconds.

    Returns:
        Callable: The decorator function.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str, *args, **kwargs) -> str:
            """
            Checks if the result is cached and returns it, or invokes the decorated method
            and caches the result with the specified expiration time.

            Args:
                url (str): The URL for which to cache the result.
                *args: Variable positional arguments.
                **kwargs: Variable keyword arguments.

            Returns:
                str: The result of the decorated method.
            """
            result_key = f"result:{url}"
            cached_result = method._redis.get(result_key)
            if cached_result is not None:
                return cached_result.decode('utf-8')
            
            result = method(url, *args, **kwargs)
            method._redis.setex(result_key, expiration_time, result)
            return result
        return wrapper
    return decorator

@count_accesses
@cache_result(10)
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL using the requests module.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the specified URL.
    """
    response = requests.get(url)
    return response.text

def replay(fn: Callable) -> None:
    """
    Displays the call history of a method.

    Args:
        fn (Callable): The method to display the call history for.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))
