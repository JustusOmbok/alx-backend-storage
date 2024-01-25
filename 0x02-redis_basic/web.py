#!/usr/bin/env python3
'''A module providing tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-level Redis instance.
'''

def data_cache(method: Callable) -> Callable:
    '''Decorator to cache the output of fetched data.
    
    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''Wrapper function for caching the output.
        
        Args:
            url (str): The URL for which to cache the result.
        
        Returns:
            str: The cached or fetched result.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper

@data_cache
def get_page(url: str) -> str:
    '''Fetches the content of a URL and caches the response,
    while tracking the request.
    
    Args:
        url (str): The URL to fetch.

    Returns:
        str: The content of the specified URL.
    '''
    return requests.get(url).text
