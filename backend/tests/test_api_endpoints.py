import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_cyclones():
    resp = client.get("/api/v1/cyclones")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert data[0]["id"] == "CYCLONE-DEMO-01"

    detail = client.get("/api/v1/cyclones/CYCLONE-DEMO-01")
    assert detail.status_code == 200
    d = detail.json()
    assert "projected_track" in d
    assert "forecast_cone" in d

def test_api_risk_and_map():
    resp = client.get("/api/v1/risk")
    assert resp.status_code == 200
    r = resp.json()
    assert 0.0 <= r["risk_score"] <= 1.0

    map_resp = client.get("/api/v1/risk/map")
    assert map_resp.status_code == 200
    assert map_resp.json()["type"] == "FeatureCollection"

def test_api_infrastructure():
    resp = client.get("/api/v1/infrastructure/hospitals")
    assert resp.status_code == 200
    assert len(resp.json()) == 12

    roads = client.get("/api/v1/infrastructure/roads")
    assert roads.status_code == 200
    assert len(roads.json()) == 45

def test_api_simulation():
    payload = {
        "wind_speed_kmh": 160.0,
        "rainfall_total_mm": 234.0,
        "storm_surge_m": 3.2
    }
    resp = client.post("/api/v1/simulation", json=payload)
    assert resp.status_code == 200
    sim = resp.json()
    assert "deltas" in sim
    assert sim["deltas"]["flooded_area_change_pct"] > 0

def test_api_agent_analyze():
    payload = {"query": "Which hospitals could become inaccessible?"}
    resp = client.post("/api/v1/agent/analyze", json=payload)
    assert resp.status_code == 200
    res = resp.json()
    assert "inaccessible_hospitals" in res["structured_evidence"]
    assert res["output_validation"]["passed"] is True

def test_api_advisory_approval_and_audit():
    advisories = client.get("/api/v1/advisories").json()
    assert len(advisories) >= 1
    adv_id = advisories[0]["id"]

    # Approve
    appr_resp = client.post(f"/api/v1/advisories/{adv_id}/approve", json={"decision_notes": "Approved for emergency broadcast"})
    assert appr_resp.status_code == 200
    assert appr_resp.json()["status"] == "APPROVED"

    # Verify audit log
    audit = client.get("/api/v1/audit").json()
    assert len(audit) >= 1
    assert any(log["action"] == "APPROVE_ADVISORY" for log in audit)
