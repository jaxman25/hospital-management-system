from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import models here
from .doctor import Doctor
from .patient import Patient

__all__ = ["Base", "Doctor", "Patient"]

from .appointment import Appointment
__all__.append('Appointment')
