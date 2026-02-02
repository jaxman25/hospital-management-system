from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

# Import after creating
from database import SessionLocal, engine
import models

# Import routers
from api.test import router as test_router
from api.patients import router as patients_router
from api.doctors import router as doctors_router

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Hospital Management System Starting...")
    # Create sample data
    try:
        db = SessionLocal()
        # Check if we have any doctors, if not create sample
        if db.query(models.Doctor).count() == 0:
            print("Creating sample data...")
            sample_doctor = models.Doctor(
                id=str(uuid.uuid4()),
                license_number="DOC-001",
                first_name="John",
                last_name="Smith",
                specialization="Cardiology",
                department="Cardiology",
                consultation_fee=100.0,
                is_available=True
            )
            db.add(sample_doctor)
            db.commit()
            print("Sample doctor created!")
    except Exception as e:
        print(f"Error creating sample data: {e}")
    finally:
        db.close()
    
    yield
    
    # Shutdown
    print("Hospital Management System Shutting Down...")

app = FastAPI(
    title="Hospital Management System API",
    version="1.0.0",
    description="Comprehensive HMS with Patient, Doctor, Appointment, and Medical Records management",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Hospital Management System API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "hospital-management-api"
    }

# Include routers
app.include_router(test_router, prefix="/api/v1")
app.include_router(patients_router, prefix="/api/v1")
app.include_router(doctors_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
