from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/test")
async def test_endpoint():
    return {"message": "API is working!", "database": "test endpoint"}

@router.get("/test-db")
async def test_db_endpoint(db: Session = Depends(get_db)):
    try:
        # Try a simple query to test database connection
        result = db.execute("SELECT 1")
        return {"message": "Database connected successfully!", "test_query": "SELECT 1 worked"}
    except Exception as e:
        return {"message": "Database connection error", "error": str(e)}
