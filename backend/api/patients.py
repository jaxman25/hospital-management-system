from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/patients")
async def get_patients(db: Session = Depends(get_db)):
    return {"message": "Patients endpoint - work in progress"}

@router.post("/patients")
async def create_patient():
    return {"message": "Create patient endpoint"}
