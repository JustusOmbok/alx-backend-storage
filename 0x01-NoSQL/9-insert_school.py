#!/usr/bin/env python3
'''Task 9's module.
'''


def insert_school(mongo_collection, **kwargs):
    '''Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object.
        **kwargs: Keyword arguments representing the fields of the new document.

    Returns:
        str: The new _id of the inserted document.
    '''
    new_school = kwargs
    result = mongo_collection.insert_one(new_school)
    return result.inserted_id
