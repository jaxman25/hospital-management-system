from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/doctors")
async def get_doctors(db: Session = Depends(get_db)):
    return {"message": "Doctors endpoint - work in progress"}
