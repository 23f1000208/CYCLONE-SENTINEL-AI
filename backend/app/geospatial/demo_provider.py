from datetime import datetime, timezone
from typing import Dict, Any, Optional
import numpy as np
from app.geospatial.provider_interface import GeospatialDataProvider

class DemoDataProvider(GeospatialDataProvider):
    """
    Deterministic Synthetic / Demo Data Provider.
    Used when live Google Earth Engine credentials are not provided or unavailable.
    Guarantees 100% offline hackathon repeatability with realistic coastal Bay of Bengal physics.
    """

    def get_elevation_grid(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> Dict[str, Any]:
        lats = np.linspace(min_lat, max_lat, 20)
        lons = np.linspace(min_lon, max_lon, 20)
        
        # Synthetic coastal elevation: drops toward coast (lon > 86.4 is ocean/coast)
        grid = []
        for lat in lats:
            row = []
            for lon in lons:
                # Coastal slope: higher in west (inland), low in east (coast/delta)
                elev = max(0.5, round(float(12.0 - (lon - min_lon) * 8.5 + (lat - min_lat) * 2.0), 2))
                row.append(elev)
            grid.append(row)

        return {
            "min_lat": min_lat,
            "min_lon": min_lon,
            "max_lat": max_lat,
            "max_lon": max_lon,
            "resolution_deg": round((max_lat - min_lat) / 20.0, 4),
            "elevation_matrix_m": grid,
            "provenance_status": "SYNTHETIC",
            "provenance_source": "Sentinel-Synthetic-SRTM30m-Demo",
            "data_freshness": "SIMULATED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_satellite_imagery_layer(self, region_id: str, date_str: Optional[str] = None) -> Dict[str, Any]:
        return {
            "region_id": region_id,
            "sensor": "Sentinel-2 Multi-Spectral / Synthetic GEE Tile",
            "tile_url_template": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "bands": ["B4", "B3", "B2", "B8_NIR"],
            "cloud_cover_pct": 14.2,
            "provenance_status": "SYNTHETIC",
            "provenance_source": "Demo Earth Engine Provider",
            "data_freshness": "SIMULATED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_land_cover_classification(self, region_id: str) -> Dict[str, Any]:
        return {
            "region_id": region_id,
            "classes": {
                "water_estuary_pct": 18.5,
                "mangrove_wetland_pct": 14.0,
                "urban_settlement_pct": 22.5,
                "agricultural_paddy_pct": 45.0
            },
            "roughness_coefficient_mannings": 0.035, # For overland flood propagation
            "provenance_status": "SYNTHETIC",
            "provenance_source": "Demo ESA WorldCover 10m",
            "data_freshness": "SIMULATED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_precipitation_accumulation(self, cyclone_id: str) -> Dict[str, Any]:
        return {
            "cyclone_id": cyclone_id,
            "max_accumulation_24h_mm": 215.0,
            "mean_accumulation_24h_mm": 165.0,
            "high_intensity_core_radius_km": 65.0,
            "radar_reflectivity_dbz_peak": 54.0,
            "provenance_status": "SYNTHETIC",
            "provenance_source": "Synthetic GPM/IMERG Rainfall Engine",
            "data_freshness": "SIMULATED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider_type": "DemoDataProvider",
            "is_live": False,
            "status": "OPERATIONAL_OFFLINE",
            "message": "Live GEE credentials not configured — using realistic Bay of Bengal synthetic demo data.",
            "provenance_status": "SYNTHETIC",
            "data_freshness": "SIMULATED"
        }
