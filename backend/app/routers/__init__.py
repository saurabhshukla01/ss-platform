from fastapi import APIRouter

from app.routers import auth, services, inquiries, crm, analytics

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(services.router)
api_router.include_router(inquiries.router)
api_router.include_router(crm.router)
api_router.include_router(analytics.router)
