from .dashboard import router as dashboard_router
from .doctors import router as doctors_router
from .patients import router as patients_router

__all__ = ["dashboard_router", "doctors_router", "patients_router"]
