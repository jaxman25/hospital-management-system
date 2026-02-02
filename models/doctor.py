from sqlalchemy import Column, Integer, String, Date
from . import Base

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    created_at = Column(Date)
