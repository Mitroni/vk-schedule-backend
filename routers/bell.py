from fastapi import APIRouter
from google_sheets import get_timetable_data
from schedule_parser import load_timetable

router = APIRouter(prefix="/api/bell", tags=["bell"])

@router.get("/")
async def bell_schedule():
    data = get_timetable_data()
    if not data:
        return {}
    # Просто возвращаем сырые данные, но можно отформатировать
    timetable = {}
    for row in data:
        if len(row) >= 2:
            pair = row[0].strip()
            time_range = row[1].strip()
            if pair and time_range and not pair.lower().startswith("перерыв"):
                timetable[pair] = time_range
    return timetable