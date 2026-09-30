import pytest
from app.risk.engine import DeterministicRiskEngine
from app.risk.weights import DEFAULT_RISK_WEIGHTS
from app.geospatial.spatial_ops import haversine_distance_km, create_circular_buffer_polygon, point_in_geojson_polygon
from app.geospatial.router import RouteAndFacilityRouter

def test_deterministic_risk_calculation():
    # Baseline condition: Wind 140, Rain 180, Surge 2.5
    result = DeterministicRiskEngine.assess_risk(
        wind_speed_kmh=140.0,
        rainfall_mm=180.0,
        storm_surge_m=2.5,
        avg_elevation_m=4.2,
        exposed_pop_ratio=0.68,
        exposed_infra_ratio=0.55,
        road_inaccessible_ratio=0.31,
        vulnerable_pop_ratio=0.28,
        weights=DEFAULT_RISK_WEIGHTS
    )
    
    assert 0.0 <= result["risk_score"] <= 1.0
    assert result["risk_category"] in ["LOW", "MEDIUM", "HIGH", "EXTREME"]
    assert "contributing_factors" in result
    assert "contributions_percent" in result
    # Check that sum of contribution percentages is ~100%
    pct_sum = sum(result["contributions_percent"].values())
    assert abs(pct_sum - 100.0) < 0.1
    assert result["confidence_score"] >= 0.70

def test_haversine_distance():
    # Puri (19.81, 85.83) to Paradeep (20.30, 86.61)
    dist = haversine_distance_km(19.81, 85.83, 20.30, 86.61)
    # Expected distance is around 97-105 km
    assert 90.0 < dist < 115.0

def test_buffer_and_polygon_containment():
    center_lat, center_lon = 20.0, 86.0
    buffer_poly = create_circular_buffer_polygon(center_lat, center_lon, radius_km=25.0)
    
    # Point at center must be inside
    assert point_in_geojson_polygon(20.0, 86.0, buffer_poly) is True
    # Point 50 km away must be outside
    assert point_in_geojson_polygon(20.5, 86.5, buffer_poly) is False

def test_router_hospital_and_shelter():
    hospitals = [
        {"id": "H-1", "name": "General Hospital", "lat": 20.0, "lon": 86.0, "elevation_m": 2.0, "bed_capacity": 100, "inundation_risk": 0.85, "is_accessible": False},
        {"id": "H-2", "name": "Inland Apex Hospital", "lat": 20.2, "lon": 86.1, "elevation_m": 8.0, "bed_capacity": 300, "inundation_risk": 0.10, "is_accessible": True},
    ]
    alternates = RouteAndFacilityRouter.find_alternate_hospitals("H-1", hospitals, flooded_road_ids=[])
    assert len(alternates) == 1
    assert alternates[0]["hospital_id"] == "H-2"
