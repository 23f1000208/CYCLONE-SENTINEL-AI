from fastapi import APIRouter
from app.api.v1.cyclones import router as cyclones_router
from app.api.v1.risk import router as risk_router
from app.api.v1.infrastructure import router as infrastructure_router
from app.api.v1.simulation import router as simulation_router
from app.api.v1.agent import router as agent_router
from app.api.v1.advisories import router as advisories_router
from app.api.v1.audit import router as audit_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(cyclones_router)
api_v1_router.include_router(risk_router)
api_v1_router.include_router(infrastructure_router)
api_v1_router.include_router(simulation_router)
api_v1_router.include_router(agent_router)
api_v1_router.include_router(advisories_router)
api_v1_router.include_router(audit_router)
