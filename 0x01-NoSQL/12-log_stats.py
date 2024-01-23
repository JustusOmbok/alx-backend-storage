#!/usr/bin/env python3
'''Script to provide stats about Nginx logs stored in MongoDB.
'''

from pymongo import MongoClient

def log_stats(mongo_collection):
    '''Displays stats about Nginx logs.

    Args:
        mongo_collection: The pymongo collection object.
    '''
    total_logs = mongo_collection.count_documents({})
    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))
