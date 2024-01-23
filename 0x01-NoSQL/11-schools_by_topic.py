#!/usr/bin/env python3
'''Task 11's module.
'''

def schools_by_topic(mongo_collection, topic):
    '''Returns the list of schools having a specific topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search.

    Returns:
        list: List of schools matching the specified topic.
    '''
    query = {"topics": {"$in": [topic]}}
    schools = list(mongo_collection.find(query))
    return schools
