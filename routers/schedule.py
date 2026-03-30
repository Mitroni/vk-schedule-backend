from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from schedule_parser import parse_schedule, find_date_in_schedule, format_schedule
from gsheets import get_students_data
from utils.cache import ttl_cache
from config import CACHE_TTL_SECONDS

router = APIRouter(prefix="/api/schedule", tags=["schedule"])

@ttl_cache(CACHE_TTL_SECONDS)
def get_parsed_schedule():
    data = get_schedule_data()
    if not data:
        return {}
    timetable_data = get_timetable_data()
    if timetable_data:
        from schedule_parser import load_timetable
        load_timetable(timetable_data)
    return parse_schedule(data)

@router.get("/date")
async def schedule_for_date(date: str = Query(..., description="YYYY-MM-DD")):
    try:
        target = datetime.strptime(date, "%Y-%m-%d").date()
    except:
        return {"error": "Invalid date format"}
    schedule = get_parsed_schedule()
    pairs = find_date_in_schedule(schedule, target)
    if pairs is None:
        return {"date": date, "pairs": []}
    return {"date": date, "pairs": pairs, "formatted": format_schedule(target, pairs)}

@router.get("/range")
async def schedule_range(start: str, end: str):
    # start и end YYYY-MM-DD
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except:
        return {"error": "Invalid date format"}
    result = []
    schedule = get_parsed_schedule()
    delta = timedelta(days=1)
    current = start_date
    while current <= end_date:
        pairs = find_date_in_schedule(schedule, current)
        result.append({
            "date": current.isoformat(),
            "pairs": pairs or [],
            "has_schedule": pairs is not None
        })
        current += delta
    return result
