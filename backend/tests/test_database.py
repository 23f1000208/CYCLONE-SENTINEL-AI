import pytest
from app.database.session import SessionLocal
import app.models as models

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_cyclone_demo_exists(db_session):
    cyclone = db_session.query(models.CycloneEvent).filter_by(id="CYCLONE-DEMO-01").first()
    assert cyclone is not None
    assert cyclone.name == "Cyclone DEMO-01"
    assert cyclone.current_wind_speed_kmh == 140.0
    assert cyclone.provenance_status == "SYNTHETIC"

def test_forecast_observations(db_session):
    forecasts = db_session.query(models.ForecastObservation).filter_by(cyclone_id="CYCLONE-DEMO-01").all()
    assert len(forecasts) >= 5
    lead_times = [f.lead_time_hours for f in forecasts]
    assert 0 in lead_times
    assert 6 in lead_times

def test_infrastructure_counts(db_session):
    hospitals = db_session.query(models.Hospital).all()
    shelters = db_session.query(models.Shelter).all()
    roads = db_session.query(models.RoadSegment).all()
    power = db_session.query(models.PowerInfrastructure).all()
    
    assert len(hospitals) == 12
    assert len(shelters) == 8
    assert len(roads) == 45
    assert len(power) == 15

def test_draft_alert_and_audit(db_session):
    alert = db_session.query(models.Alert).filter_by(cyclone_id="CYCLONE-DEMO-01").first()
    assert alert is not None
    assert alert.status in ["DRAFT", "APPROVED"]
    assert alert.is_official_government_warning in [False, True]
    
    audit = db_session.query(models.AuditLog).first()
    assert audit is not None
    assert len(audit.checksum) == 64
