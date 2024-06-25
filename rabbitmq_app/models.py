# server/app/models.py
from pydantic import BaseModel
from datetime import datetime

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime
