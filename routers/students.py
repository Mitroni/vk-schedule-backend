from fastapi import APIRouter

router = APIRouter(prefix="/api/students", tags=["students"])

@router.get("/")
async def get_students(vk_user_id: int):
    return [{"full_name": "Test Student", "certificate": "Yes"}]
