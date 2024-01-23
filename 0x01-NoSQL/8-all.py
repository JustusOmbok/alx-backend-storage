#!/usr/bin/env python3
""" Module for 8-all """


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        List[dict]: A list containing all documents in the collection.
    """
    return [doc for docs in mongo_collection.find()]
