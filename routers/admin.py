from fastapi import APIRouter, Depends, HTTPException
from auth import is_admin
from utils.cache import ttl_cache
from gsheets import get_schedule_data, get_timetable_data, get_students_data
from schedule_parser import parse_schedule, load_timetable

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/refresh")
async def refresh_data(vk_user_id: int):
    if not is_admin(vk_user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    # Очистка кэша (просто перезапись)
    # Можно инвалидировать декоратор, но проще перезагрузить все данные в память
    # В реальном проекте используйте глобальные переменные или Redis
    # Здесь для простоты используем функцию, которая перезапишет кэш при следующем вызове
    # Вызываем все функции, чтобы обновить кэш
    get_schedule_data()
    get_timetable_data()
    get_students_data()
    # Принудительно перечитать расписание звонков в парсере
    timetable_data = get_timetable_data()
    if timetable_data:
        load_timetable(timetable_data)
    parse_schedule(get_schedule_data())  # пересоздаст кэш
    return {"status": "refreshed"}
