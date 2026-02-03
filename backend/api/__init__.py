from .patients import router as patients_router
from .doctors import router as doctors_router
from .appointments import router as appointments_router

__all__ = ["patients_router", "doctors_router", "appointments_router"]
