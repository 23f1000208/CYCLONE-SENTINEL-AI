from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.seed_demo import seed_demo_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist and seed demo data automatically on every boot
    seed_demo_data()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Cyclone Impact & Infrastructure Vulnerability Forecaster — Anticipatory Action Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - allow all origins for local hackathon development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "disclaimer": "MODELLED SCENARIO DECISION SUPPORT — NOT AN OFFICIAL FORECAST"
    }

@app.get("/", tags=["System"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "tagline": settings.TAGLINE,
        "docs": "/docs",
        "health": "/health"
    }

from app.api.v1.router import api_v1_router

app.include_router(api_v1_router)
