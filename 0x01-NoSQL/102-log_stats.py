#!/usr/bin/env python3
'''Script to provide stats about Nginx logs, including the top 10 IPs.
'''

from pymongo import MongoClient
from collections import Counter

def log_stats(mongo_collection):
    '''Displays stats about Nginx logs, including the top 10 IPs.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object.
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

    # Find the top 10 most present IPs
    ip_counter = Counter(log['ip'] for log in mongo_collection.find())
    top_ips = ip_counter.most_common(10)

    print("IPs:")
    for ip, count in top_ips:
        print("\t{}: {}".format(ip, count))

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    log_stats(logs_collection)
