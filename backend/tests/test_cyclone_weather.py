import pytest
from app.database.session import SessionLocal
from app.geospatial.demo_provider import DemoDataProvider
from app.geospatial.gee_provider import EarthEngineProvider
from app.services.cyclone_service import CycloneService

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_demo_data_provider():
    provider = DemoDataProvider()
    dem = provider.get_elevation_grid(19.5, 85.5, 20.5, 86.5)
    assert "elevation_matrix_m" in dem
    assert len(dem["elevation_matrix_m"]) == 20
    assert dem["provenance_status"] == "SYNTHETIC"
    
    land_cover = provider.get_land_cover_classification("REGION-ODISHA-COASTAL")
    assert "classes" in land_cover
    assert land_cover["classes"]["mangrove_wetland_pct"] > 0

def test_gee_provider_graceful_fallback():
    provider = EarthEngineProvider()
    status = provider.get_provider_status()
    assert "provider_type" in status
    assert status["provenance_status"] in ["SYNTHETIC", "OBSERVED"]
    if not status["is_live"]:
        assert "Live data unavailable" in status["message"]

def test_cyclone_service(db_session):
    details = CycloneService.get_cyclone_details(db_session, "CYCLONE-DEMO-01")
    assert details is not None
    assert details["name"] == "Cyclone DEMO-01"
    assert len(details["historical_track"]) >= 3
    assert len(details["projected_track"]) >= 2
    assert len(details["forecast_cone"]) >= 2
    assert details["wind_field_geojson"]["type"] == "Polygon"
