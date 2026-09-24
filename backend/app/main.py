from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# =========================================================
# ROUTERS
# =========================================================

from app.routers.auth import router as auth_router
from app.routers.services import router as services_router
from app.routers.inquiries import router as inquiries_router
from app.routers.crm import router as crm_router
from app.routers.analytics import router as analytics_router
from app.routers.website import router as website_router
from app.routers import api_router


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="""
SS Platform API

Backend API for:

- Authentication
- Services
- Inquiries
- CRM
- Analytics
- Website Content
""",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# API PREFIX
# =========================================================

API_PREFIX = settings.API_V1_PREFIX


# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    auth_router,
    prefix=API_PREFIX,
)

app.include_router(
    services_router,
    prefix=API_PREFIX,
)

app.include_router(
    inquiries_router,
    prefix=API_PREFIX,
)

app.include_router(
    crm_router,
    prefix=API_PREFIX,
)

app.include_router(
    analytics_router,
    prefix=API_PREFIX,
)

app.include_router(
    website_router,
    prefix=API_PREFIX,
)

app.include_router(
    api_router,
    prefix=API_PREFIX,
)

# =========================================================
# SYSTEM ROUTES
# =========================================================

@app.get("/", tags=["System"])
def root():
    return {
        "message": "SS Platform API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "ok",
        "service": "SS Platform API",
    }