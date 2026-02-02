from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    emergency_contact = Column(String)
    blood_type = Column(String)
    created_at = Column(Date)
