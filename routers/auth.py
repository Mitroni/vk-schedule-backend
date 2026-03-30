from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, UserLink
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LinkRequest(BaseModel):
    vk_user_id: int
    full_name: str

@router.post("/link")
async def link_user(request: LinkRequest, db: Session = Depends(get_db)):
    # Проверяем, есть ли уже связь
    existing = db.query(UserLink).filter(UserLink.vk_user_id == request.vk_user_id).first()
    if existing:
        existing.full_name = request.full_name
        db.commit()
        return {"status": "updated"}
    new_link = UserLink(vk_user_id=request.vk_user_id, full_name=request.full_name)
    db.add(new_link)
    db.commit()
    return {"status": "created"}

@router.get("/me")
async def get_me(vk_user_id: int, db: Session = Depends(get_db)):
    link = db.query(UserLink).filter(UserLink.vk_user_id == vk_user_id).first()
    if link:
        return {"full_name": link.full_name, "is_linked": True}
    return {"is_linked": False}