from fastapi import APIRouter

from routers import upload, auth

router = APIRouter()
router.include_router(upload.router, tags=["Upload"], prefix='/upload')
router.include_router(auth.router, tags=["Auth"], prefix='/auth')
