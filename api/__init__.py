from fastapi import APIRouter

from api.user_auth import router as auth_router
from api.products import router as product_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(product_router)
