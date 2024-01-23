#!/usr/bin/env python3
'''Task 101's module.
'''

def top_students(mongo_collection):
    '''Returns all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        list: List of students sorted by average score with 'averageScore'.
    '''
    pipeline = [
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    students = list(mongo_collection.aggregate(pipeline))
    return students
