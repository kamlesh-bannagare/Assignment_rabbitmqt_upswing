# server/app/routes.py
from fastapi import APIRouter, HTTPException, Query
from Assignment_rabbitmqt_upswing.rabbitmq_app.database import collection
from typing import Annotated
from datetime import datetime, timezone

router = APIRouter()
"""
this will get data from database and aggregate on it and will return result with
 
"""
@router.get("/status_count/")
async def get_status_count(start_time: datetime = Query(...), end_time: datetime = Query(...)):
    print(start_time)
    print(type(start_time))
    pipeline = [
        {"$match": {"timestamp": {"$gte": start_time.timestamp(), "$lte": end_time.timestamp()}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    result = list(collection.aggregate(pipeline))
    result_data= {}

    for item in result:
        result_data[item['_id']] = item['count']

    return result_data
