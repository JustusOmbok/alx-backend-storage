#!/usr/bin/env python3
""" Module for 8-all """
from pymongo.collection import Collection
from typing import List


def list_all(mongo_collection: Collection) -> List[dict]:
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        List[dict]: A list containing all documents in the collection.
    """
    documents = list(mongo_collection.find())
    return documents
