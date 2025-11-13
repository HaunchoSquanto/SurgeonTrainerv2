"""Routes package."""
from fastapi import APIRouter

# Import all route modules
from .patients import router as patients_router
from .encounters import router as encounters_router
from .diagnoses import router as diagnoses_router
from .procedures import router as procedures_router
from .rc_rotatorcuff import router as rc_rotatorcuff_router
from .rc_kneescope import router as rc_kneescope_router
from .rc_shoulderscope import router as rc_shoulderscope_router
from .rc_shoulderarthroplasty import router as rc_shoulderarthroplasty_router
from .rc_hipscope import router as rc_hipscope_router
from .rc_hiparthroplasty import router as rc_hiparthroplasty_router
from .rc_kneearthroplasty import router as rc_kneearthroplasty_router
from .rc_other import router as rc_other_router

# Create main router
router = APIRouter()

# Health check endpoint
@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "SurgeonTrainer API"}

# Include all routers
router.include_router(patients_router, prefix="/patients", tags=["Patients"])
router.include_router(encounters_router, prefix="/encounters", tags=["Encounters"])
router.include_router(diagnoses_router, prefix="/diagnoses", tags=["Diagnoses"])
router.include_router(procedures_router, prefix="/procedures", tags=["Procedures"])
router.include_router(rc_rotatorcuff_router, prefix="/rc/rotator-cuff", tags=["Research Cases - Rotator Cuff"])
router.include_router(rc_kneescope_router, prefix="/rc/knee-surgical", tags=["Research Cases - Knee Surgical"])
router.include_router(rc_shoulderscope_router, prefix="/rc/shoulder-scope", tags=["Research Cases - Shoulder Scope"])
router.include_router(rc_shoulderarthroplasty_router, prefix="/rc/shoulder-arthroplasty", tags=["Research Cases - Shoulder Arthroplasty"])
router.include_router(rc_hipscope_router, prefix="/rc/hip-scope", tags=["Research Cases - Hip Scope"])
router.include_router(rc_hiparthroplasty_router, prefix="/rc/hip-arthroplasty", tags=["Research Cases - Hip Arthroplasty"])
router.include_router(rc_kneearthroplasty_router, prefix="/rc/knee-arthroplasty", tags=["Research Cases - Knee Arthroplasty"])
router.include_router(rc_other_router, prefix="/rc/other", tags=["Research Cases - Other Procedures"])

__all__ = ["router"]
