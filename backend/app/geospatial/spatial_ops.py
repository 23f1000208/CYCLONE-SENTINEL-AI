import math
from typing import List, Tuple, Dict, Any
from shapely.geometry import Point, Polygon, LineString, mapping, shape
import numpy as np

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Great Circle distance between two coordinates in kilometers."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 3)

def create_circular_buffer_polygon(center_lat: float, center_lon: float, radius_km: float, num_points: int = 32) -> Dict[str, Any]:
    """Create a GeoJSON Polygon representing a circular buffer (e.g. wind radius or surge zone)."""
    coords = []
    # 1 deg lat ~ 111 km, 1 deg lon ~ 111 * cos(lat) km
    lat_deg = radius_km / 111.0
    lon_deg = radius_km / (111.0 * math.cos(math.radians(center_lat)))
    
    for i in range(num_points):
        theta = 2.0 * math.pi * i / num_points
        dlat = lat_deg * math.sin(theta)
        dlon = lon_deg * math.cos(theta)
        coords.append([round(center_lon + dlon, 5), round(center_lat + dlat, 5)])
    
    coords.append(coords[0]) # Close ring
    return {
        "type": "Polygon",
        "coordinates": [coords]
    }

def point_in_geojson_polygon(lat: float, lon: float, geojson_polygon: Dict[str, Any]) -> bool:
    """Test if a lat/lon point lies inside a GeoJSON Polygon."""
    p = Point(lon, lat) # Shapely uses (x, y) = (lon, lat)
    poly = shape(geojson_polygon)
    return poly.contains(p) or poly.touches(p)
