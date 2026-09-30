from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
import app.models as models
from app.services.cyclone_service import CycloneService

router = APIRouter(prefix="/cyclones", tags=["Cyclone Tracking"])

@router.get("", response_model=List[Dict[str, Any]])
def list_cyclones(db: Session = Depends(get_db)):
    cyclones = db.query(models.CycloneEvent).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "category": c.category,
            "basin": c.basin,
            "current_lat": c.current_lat,
            "current_lon": c.current_lon,
            "wind_speed_kmh": c.current_wind_speed_kmh,
            "pressure_hpa": c.current_pressure_hpa,
            "movement": f"{c.movement_direction} at {c.movement_speed_kmh} km/h",
            "data_freshness": c.data_freshness,
            "provenance_status": c.provenance_status,
            "last_updated": c.last_updated.isoformat()
        }
        for c in cyclones
    ]

@router.get("/{cyclone_id}")
def get_cyclone_details(cyclone_id: str, db: Session = Depends(get_db)):
    details = CycloneService.get_cyclone_details(db, cyclone_id)
    if not details:
        raise HTTPException(status_code=404, detail="Cyclone not found")
    return details
