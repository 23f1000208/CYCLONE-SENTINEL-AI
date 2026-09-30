from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
import app.models as models
from app.risk.engine import DeterministicRiskEngine

router = APIRouter(prefix="/risk", tags=["Risk Modeling"])

@router.get("")
def get_current_risk(db: Session = Depends(get_db)):
    risk = db.query(models.RiskAssessment).order_by(models.RiskAssessment.assessed_at.desc()).first()
    if not risk:
        return {"message": "No risk assessment available"}
    return {
        "id": risk.id,
        "cyclone_id": risk.cyclone_id,
        "region_id": risk.region_id,
        "risk_score": risk.risk_score,
        "risk_category": risk.risk_category,
        "confidence_score": risk.confidence_score,
        "hazard_score": risk.hazard_score,
        "exposure_score": risk.exposure_score,
        "vulnerability_score": risk.vulnerability_score,
        "contributing_factors": risk.contributing_factors,
        "formula": risk.formula_used,
        "model_version": risk.model_version,
        "provenance_status": risk.provenance_status,
        "assessed_at": risk.assessed_at.isoformat()
    }

@router.get("/map")
def get_risk_map_layers(db: Session = Depends(get_db)):
    zones = db.query(models.PopulationZone).all()
    hazards = db.query(models.HazardZone).all()
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": z.boundary_geojson,
                "properties": {
                    "id": z.id,
                    "name": z.zone_name,
                    "population": z.total_population,
                    "exposed_population": z.exposed_population,
                    "risk_tier": "HIGH" if z.exposed_population > 40000 else "MEDIUM"
                }
            }
            for z in zones
        ]
    }
