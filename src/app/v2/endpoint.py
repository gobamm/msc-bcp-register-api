from fastapi import APIRouter
from v2.routes import register

api_router = APIRouter()

api_router.include_router(
    register.router,
    prefix="/v2",
    tags=["register"]
)
