from fastapi import APIRouter
router = APIRouter(prefix="/api/admin", tags=["admin"])
@router.post("/refresh")
async def refresh_data(vk_user_id: int):
    return {"status": "ok"}
