from fastapi import APIRouter
router = APIRouter(prefix="/api/schedule", tags=["schedule"])
@router.get("/date")
async def schedule_for_date(date: str):
    return {"date": date}
@router.get("/range")
async def schedule_range(start: str, end: str):
    return [{"date": start}, {"date": end}]
