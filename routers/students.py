from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from gsheets import get_students_data
from auth import is_admin
from utils.cache import ttl_cache
from config import CACHE_TTL_SECONDS

router = APIRouter(prefix="/api/students", tags=["students"])

@ttl_cache(CACHE_TTL_SECONDS)
def get_raw_students():
    data = get_students_data()
    if not data or len(data) < 2:
        return []
    students = []
    for row in data[1:]:
        if not row[0] or not row[0].strip():
            continue
        student = {
            "full_name": row[0].strip(),
            "email": row[1].strip() if len(row) > 1 else "",
            "phone": row[2].strip() if len(row) > 2 else "",
            "certificate": row[3].strip() if len(row) > 3 else ""
        }
        students.append(student)
    return students

@router.get("/")
async def get_students(vk_user_id: int, db: Session = Depends(get_db)):
    raw_students = get_raw_students()
    if is_admin(vk_user_id):
        return raw_students
    filtered = []
    for s in raw_students:
        filtered.append({
            "full_name": s["full_name"],
            "certificate": s["certificate"]
        })
    return filtered
