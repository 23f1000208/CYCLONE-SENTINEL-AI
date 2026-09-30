from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
import app.models as models

router = APIRouter(prefix="/infrastructure", tags=["Infrastructure Vulnerability"])

@router.get("")
def list_infrastructure_summary(db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).count()
    shelters = db.query(models.Shelter).count()
    roads = db.query(models.RoadSegment).count()
    power = db.query(models.PowerInfrastructure).count()
    
    inacc_hosp = db.query(models.Hospital).filter_by(is_accessible=False).count()
    flooded_roads = db.query(models.RoadSegment).filter_by(passability_status="IMPASSABLE_FLOODED").count()
    
    return {
        "hospitals_total": hospitals,
        "hospitals_inaccessible": inacc_hosp,
        "shelters_total": shelters,
        "roads_total": roads,
        "roads_impassable": flooded_roads,
        "power_assets_total": power
    }

@router.get("/hospitals")
def get_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).all()
    return [
        {
            "id": h.id,
            "name": h.name,
            "lat": h.lat,
            "lon": h.lon,
            "elevation_m": h.elevation_m,
            "bed_capacity": h.bed_capacity,
            "icu_capacity": h.icu_capacity,
            "is_accessible": h.is_accessible,
            "inundation_risk": h.inundation_risk,
            "emergency_generator_hours": h.emergency_generator_hours
        }
        for h in hospitals
    ]

@router.get("/shelters")
def get_shelters(db: Session = Depends(get_db)):
    shelters = db.query(models.Shelter).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "lat": s.lat,
            "lon": s.lon,
            "total_capacity": s.total_capacity,
            "current_occupancy": s.current_occupancy,
            "expected_demand": s.expected_demand,
            "medical_facility": s.medical_facility,
            "elevation_m": s.elevation_m,
            "is_safe": s.is_safe
        }
        for s in shelters
    ]

@router.get("/roads")
def get_roads(db: Session = Depends(get_db)):
    roads = db.query(models.RoadSegment).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "start_lat": r.start_lat,
            "start_lon": r.start_lon,
            "end_lat": r.end_lat,
            "end_lon": r.end_lon,
            "geometry": r.geometry_geojson,
            "elevation_m": r.elevation_m,
            "distance_to_coast_km": r.distance_to_coast_km,
            "critical_corridor": r.critical_evacuation_corridor,
            "passability": r.passability_status,
            "flood_depth_cm": r.current_flood_depth_cm
        }
        for r in roads
    ]

@router.get("/power")
def get_power_infrastructure(db: Session = Depends(get_db)):
    power = db.query(models.PowerInfrastructure).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "lat": p.lat,
            "lon": p.lon,
            "elevation_m": p.elevation_m,
            "population_served": p.population_served,
            "is_operational": p.is_operational,
            "flood_risk": p.flood_risk
        }
        for p in power
    ]
