from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class TrackPoint(BaseModel):
    lead_time_hours: int
    valid_time: str
    lat: float
    lon: float
    wind_speed_kmh: float
    pressure_hpa: float
    cone_radius_km: float
    uncertainty_score: float

class CycloneResponse(BaseModel):
    id: str
    name: str
    status: str
    category: str
    basin: str
    current_location: Dict[str, float]
    current_wind_speed_kmh: float
    current_pressure_hpa: float
    movement_direction: str
    movement_speed_kmh: float
    wind_radius_km: float
    provenance_status: str
    provenance_source: str
    data_freshness: str
    last_updated: str
    historical_track: List[TrackPoint]
    projected_track: List[TrackPoint]
    forecast_cone: List[Dict[str, Any]]
    wind_field_geojson: Dict[str, Any]
