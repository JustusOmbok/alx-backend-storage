#!/usr/bin/env python3

import requests
import redis
import time
from functools import wraps
from typing import Callable

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

def main() -> None:
    """
    Main function to demonstrate the usage of the get_page function with caching and access tracking.
    """
    # Initialize the Redis client
    get_page._redis = redis.Redis()

    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"
    
    # Access the URL (this will be slow due to the simulated delay)
    content = get_page(url)
    print(content)

    # Access the URL again (this time it should be cached)
    content = get_page(url)
    print(content)

    # Wait for more than 10 seconds to expire the cache
    time.sleep(11)

    # Access the URL after cache expiration (this will fetch the content again)
    content = get_page(url)
    print(content)

if __name__ == "__main__":
    main()
