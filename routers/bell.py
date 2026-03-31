from fastapi import APIRouter
router = APIRouter(prefix="/api/bell", tags=["bell"])
@router.get("/")
async def bell_schedule():
    return {"1 пара": "08:30 - 10:00"}
