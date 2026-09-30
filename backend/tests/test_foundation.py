from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    UserRole
)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == settings.PROJECT_NAME
    assert "MODELLED SCENARIO" in data["disclaimer"]

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "tagline" in response.json()

def test_password_hashing():
    pwd = "EmergencyManager2026!Secure"
    hashed = get_password_hash(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token():
    token = create_access_token("analyst_01", role=UserRole.DISASTER_MANAGER)
    payload = decode_access_token(token)
    assert payload.sub == "analyst_01"
    assert payload.role == UserRole.DISASTER_MANAGER
