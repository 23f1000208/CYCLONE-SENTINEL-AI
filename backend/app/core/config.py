import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

# Compute absolute path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_FILE = os.path.join(BASE_DIR, "cyclone_sentinel.db").replace("\\", "/")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cyclone Sentinel AI"
    TAGLINE: str = "Predict the Impact. Protect the Infrastructure. Act Before Landfall."
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(default="cyclone-sentinel-dev-secret-key-change-in-production-min-32-chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # Database (always resolves to absolute path)
    DATABASE_URL: str = Field(default=f"sqlite:///{DEFAULT_DB_FILE}")
    
    # Gemini AI
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash")
    
    # Google Earth Engine
    GEE_PROJECT_ID: Optional[str] = Field(default=None)
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = Field(default=None)
    
    # Agent & Guardrails
    MAX_AGENT_ITERATIONS: int = 5
    MIN_CONFIDENCE_THRESHOLD: float = 0.65
    REQUIRE_HUMAN_APPROVAL_FOR_ADVISORIES: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
