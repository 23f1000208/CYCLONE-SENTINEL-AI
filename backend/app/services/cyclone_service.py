import math
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import app.models as models
from app.geospatial.spatial_ops import create_circular_buffer_polygon

class CycloneService:
    @staticmethod
    def get_cyclone_details(db: Session, cyclone_id: str = "CYCLONE-DEMO-01") -> Optional[Dict[str, Any]]:
        cyclone = db.query(models.CycloneEvent).filter_by(id=cyclone_id).first()
        if not cyclone:
            return None

        forecasts = (
            db.query(models.ForecastObservation)
            .filter_by(cyclone_id=cyclone_id)
            .order_by(models.ForecastObservation.lead_time_hours)
            .all()
        )

        # Historical vs Projected tracks
        historical_track = []
        projected_track = []
        forecast_cone_polygons = []

        for f in forecasts:
            point = {
                "lead_time_hours": f.lead_time_hours,
                "valid_time": f.valid_time.isoformat(),
                "lat": f.lat,
                "lon": f.lon,
                "wind_speed_kmh": f.wind_speed_kmh,
                "pressure_hpa": f.pressure_hpa,
                "cone_radius_km": f.cone_radius_km,
                "uncertainty_score": f.uncertainty_score
            }
            if f.lead_time_hours <= 0:
                historical_track.append(point)
            else:
                projected_track.append(point)
                # Generate cone buffer for projected points
                cone_poly = create_circular_buffer_polygon(f.lat, f.lon, f.cone_radius_km)
                forecast_cone_polygons.append({
                    "lead_time_hours": f.lead_time_hours,
                    "polygon": cone_poly
                })

        # Wind field buffer (Rmax = ~35km, R64kt = ~85km, R34kt = ~150km)
        wind_field_geojson = create_circular_buffer_polygon(
            cyclone.current_lat, cyclone.current_lon, cyclone.wind_radius_km
        )

        return {
            "id": cyclone.id,
            "name": cyclone.name,
            "status": cyclone.status,
            "category": cyclone.category,
            "basin": cyclone.basin,
            "current_location": {
                "lat": cyclone.current_lat,
                "lon": cyclone.current_lon
            },
            "current_wind_speed_kmh": cyclone.current_wind_speed_kmh,
            "current_pressure_hpa": cyclone.current_pressure_hpa,
            "movement_direction": cyclone.movement_direction,
            "movement_speed_kmh": cyclone.movement_speed_kmh,
            "wind_radius_km": cyclone.wind_radius_km,
            "provenance_status": cyclone.provenance_status,
            "provenance_source": cyclone.provenance_source,
            "data_freshness": cyclone.data_freshness,
            "last_updated": cyclone.last_updated.isoformat(),
            "historical_track": historical_track,
            "projected_track": projected_track,
            "forecast_cone": forecast_cone_polygons,
            "wind_field_geojson": wind_field_geojson
        }
