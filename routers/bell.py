from fastapi import APIRouter
from gsheets import get_timetable_data

router = APIRouter(prefix="/api/bell", tags=["bell"])

@router.get("/")
async def bell_schedule():
    data = get_timetable_data()
    if not data:
        return {}
    timetable = {}
    for row in data:
        if len(row) >= 2:
            pair = row[0].strip()
            time_range = row[1].strip()
            if pair and time_range and not pair.lower().startswith("перерыв"):
                timetable[pair] = time_range
    return timetable
