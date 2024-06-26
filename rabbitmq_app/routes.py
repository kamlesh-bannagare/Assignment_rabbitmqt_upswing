from fastapi import APIRouter, HTTPException, Query
from Assignment_rabbitmqt_upswing.rabbitmq_app.database import collection
from typing import Annotated
from datetime import datetime, timezone

router = APIRouter()

"""
This API endpoint retrieves status counts from a database within a specified time range.

It accepts the following query parameters:

* start_time (datetime): The beginning of the desired time range (inclusive).
* end_time (datetime): The end of the desired time range (inclusive).

The endpoint returns a dictionary containing the count of each status value within the 
specified time range.
"""

@router.get("/status_count/")
async def get_status_count(
    start_time: Annotated[datetime, Query(..., description="Start time of the query range format (YYYY-MM-DDTHH:MM:SSZ)")] = None,
    end_time: Annotated[datetime, Query(..., description="End time of the query range format (YYYY-MM-DDTHH:MM:SSZ)")] = None,
) -> dict:
    """
    Retrieves the count of each status value within a specified time range.

    Args:
        start_time (datetime, optional): The beginning of the desired time range (inclusive) in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Defaults to None.
        end_time (datetime, optional): The end of the desired time range (inclusive) in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Defaults to None.

    Returns:
        dict: A dictionary containing the count of each status value within the specified time range.
    """

    # Print for debugging purposes (consider removing in production)
    # print(f"start_time: {start_time}, type: {type(start_time)}")
    # print(f"end_time: {end_time}, type: {type(end_time)}")

    if start_time is None or end_time is None:
        raise HTTPException(status_code=400, detail="Both start_time and end_time are required query parameters.")

    # Ensure start_time is before or equal to end_time
    if start_time > end_time:
        raise HTTPException(status_code=400, detail="start_time must be before or equal to end_time.")

    # Construct the aggregation pipeline for efficient data retrieval
    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": start_time.timestamp(),
                    "$lte": end_time.timestamp(),
                }
            }
        },
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
    ]

    # Perform the aggregation on the collection to get results
    result = list(collection.aggregate(pipeline))

    # Convert the aggregated results (list of documents) into a dictionary for easier response formatting
    result_data = {item['_id']: item['count'] for item in result}

    return result_data
