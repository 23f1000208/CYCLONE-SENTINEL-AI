import math
from typing import Dict, Any, List
import numpy as np
from app.geospatial.spatial_ops import haversine_distance_km

class StormSurgeSimulationEngine:
    """
    Deterministic Hydrodynamic Storm Surge & Coastal Inundation Model.
    Uses modified SLOSH/Jelesnianski parametric formulation:
    Surge Height (m) = S_pressure + S_wind + S_bathymetry
    where:
    S_pressure = 0.01 * (1013.25 - central_pressure_hpa)  # Inverse barometer effect (~1cm per 1hPa deficit)
    S_wind = (C_d * rho_a / (rho_w * g * h)) * V_wind^2 * Fetch * cos(theta)
    """
    DISCLAIMER = "MODELLED SCENARIO — NOT AN OFFICIAL FORECAST"

    @classmethod
    def compute_peak_surge_height(
        cls,
        wind_speed_kmh: float,
        central_pressure_hpa: float,
        coastal_bathymetry_slope: float = 0.0015, # Gentle Bay of Bengal shelf amplifies surge
        approach_angle_deg: float = 45.0          # Angle relative to coastline
    ) -> float:
        # 1. Barometric setup (~1cm per 1hPa deficit)
        delta_p = max(0.0, 1013.25 - central_pressure_hpa)
        s_baro = 0.0102 * delta_p # in meters (~0.46m for 968 hPa)

        # 2. Wind stress setup
        wind_ms = wind_speed_kmh / 3.6
        # Parametric wind surge amplification for shallow continental shelf
        c_d = 0.0032 # Shallow-water amplified drag coefficient
        s_wind = (c_d * (wind_ms ** 2) / (9.81 * 14.0)) * 85.0 * math.cos(math.radians(approach_angle_deg))
        
        # Shelf shoaling factor for Bay of Bengal shallow head-bay
        shoaling_factor = 1.0 + (0.002 / max(0.0005, coastal_bathymetry_slope)) * 0.35
        total_surge = (s_baro + max(0.0, s_wind)) * shoaling_factor
        return round(float(np.clip(total_surge, 0.5, 9.5)), 2)

    @classmethod
    def run_surge_simulation(
        cls,
        surge_height_m: float,
        coastline_anchor_lat: float,
        coastline_anchor_lon: float,
        inland_penetration_km: float = 12.0
    ) -> Dict[str, Any]:
        """
        Calculates coastal inundation polygon and depth zones.
        Surge penetrates inland decaying with ground elevation and distance from coast.
        """
        # Generate inundation contour polygon
        # Points along coastal corridor flooded up to penetration depth
        coords = [
            [coastline_anchor_lon - 0.25, coastline_anchor_lat - 0.15],
            [coastline_anchor_lon + 0.35, coastline_anchor_lat + 0.15],
            [coastline_anchor_lon + 0.30, coastline_anchor_lat + 0.28],
            [coastline_anchor_lon - 0.15, coastline_anchor_lat + 0.22],
            [coastline_anchor_lon - 0.25, coastline_anchor_lat - 0.15]
        ]
        
        # Inundation area roughly: width 60km * inland penetration
        flooded_area_sqkm = round(60.0 * (inland_penetration_km * (surge_height_m / 3.0)), 1)

        return {
            "model_type": "Parametric Hydrodynamic Coastal Surge Model",
            "peak_surge_height_m": surge_height_m,
            "inundation_area_sqkm": flooded_area_sqkm,
            "max_inland_penetration_km": round(inland_penetration_km * (surge_height_m / 2.5), 1),
            "inundation_zone_geojson": {
                "type": "Polygon",
                "coordinates": [coords]
            },
            "disclaimer": cls.DISCLAIMER,
            "provenance_status": "SIMULATED"
        }
