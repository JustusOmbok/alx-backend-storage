#!/usr/bin/env python3

import redis
from web import get_page, replay

def main():
    # Initialize the Redis client
    # get_page._redis = redis.Redis()  # Import redis module and set _redis attribute
    
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

    # Display the call history of the get_page method
    replay(get_page)

if __name__ == "__main__":
    main()
