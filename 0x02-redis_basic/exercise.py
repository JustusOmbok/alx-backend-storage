#!/usr/bin/env python3
'''Module for interacting with Redis, a NoSQL data storage.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    '''Decorator to track the number of calls made to a method in a Cache class.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.

        Args:
            self: The instance of the Cache class.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            Any: The result of the decorated method.
        '''
        # Increment the call counter in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Decorator to track the call details of a method in a Cache class.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.

        Args:
            self: The instance of the Cache class.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            Any: The result of the decorated method.
        '''
        # Define input and output Redis keys
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        
        # Store input arguments in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        
        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)
        
        # Store the output in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        
        return output
    return wrapper


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.

    Args:
        fn (Callable): The method for which to display the call history.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    
    # Get the function name and keys
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    
    # Get the function call count from Redis
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    
    # Print the call count information
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    
    # Get the inputs and outputs lists from Redis
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    
    # Print each function call with inputs and output
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    '''Represents an object for storing data in a Redis data storage.
    '''
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        # Initialize the Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used for storing the data.
        '''
        data_key = str(uuid.uuid4())
        # Set the data in Redis with a random key
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.

        Args:
            key (str): The key used for retrieving data from Redis.
            fn (Callable, optional): Optional callable to convert the data
                back to the desired format. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, possibly
                converted using the provided callable.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from a Redis data storage.

        Args:
            key (str): The key used for retrieving the string from Redis.

        Returns:
            str: The retrieved string or None if the key does not exist.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.

        Args:
            key (str): The key used for retrieving the integer from Redis.

        Returns:
            int: The retrieved integer or None if the key does not exist.
        '''
        return self.get(key, lambda x: int(x))

