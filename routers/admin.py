from fastapi import APIRouter, HTTPException
from auth import is_admin
from gsheets import get_schedule_data, get_timetable_data, get_students_data
from schedule_parser import parse_schedule, load_timetable

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/refresh")
async def refresh_data(vk_user_id: int):
    if not is_admin(vk_user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    get_schedule_data()
    get_timetable_data()
    get_students_data()
    timetable_data = get_timetable_data()
    if timetable_data:
        load_timetable(timetable_data)
    parse_schedule(get_schedule_data())
    return {"status": "refreshed"}
