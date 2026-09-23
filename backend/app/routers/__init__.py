from fastapi import APIRouter

from app.routers import (
    auth, services, categories, inquiries, crm, analytics,
    subscriptions, payments, website, content, seo, communication, settings, audit,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(services.router)
api_router.include_router(categories.router)
api_router.include_router(inquiries.router)
api_router.include_router(crm.router)
api_router.include_router(analytics.router)
api_router.include_router(subscriptions.router)
api_router.include_router(payments.router)
api_router.include_router(website.router)
api_router.include_router(content.router)
api_router.include_router(seo.router)
api_router.include_router(communication.router)
api_router.include_router(settings.router)
api_router.include_router(audit.router)
