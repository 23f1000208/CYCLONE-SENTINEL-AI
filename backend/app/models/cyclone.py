from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class CycloneEvent(Base):
    __tablename__ = "cyclone_events"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), default="ACTIVE MONITORING")  # ACTIVE MONITORING, LANDFALL, DISSIPATED
    category = Column(String(50), default="Severe Cyclonic Storm")
    basin = Column(String(50), default="Bay of Bengal")
    
    current_lat = Column(Float, nullable=False)
    current_lon = Column(Float, nullable=False)
    current_wind_speed_kmh = Column(Float, nullable=False)  # km/h
    current_pressure_hpa = Column(Float, nullable=False)    # hPa
    movement_direction = Column(String(20), default="Northwest")
    movement_speed_kmh = Column(Float, default=18.0)
    wind_radius_km = Column(Float, default=120.0)
    
    provenance_status = Column(String(30), default="SYNTHETIC")  # OBSERVED, FORECAST, MODELLED, SIMULATED, SYNTHETIC
    provenance_source = Column(String(100), default="Sentinel Disaster Simulation Engine")
    data_freshness = Column(String(30), default="SIMULATED")     # LIVE, RECENT, STALE, UNAVAILABLE, SIMULATED
    
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    forecasts = relationship("ForecastObservation", back_populates="cyclone", cascade="all, delete-orphan")
    weather_observations = relationship("WeatherObservation", back_populates="cyclone", cascade="all, delete-orphan")

class ForecastObservation(Base):
    __tablename__ = "forecast_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cyclone_id = Column(String(50), ForeignKey("cyclone_events.id"), nullable=False)
    lead_time_hours = Column(Integer, nullable=False)
    valid_time = Column(DateTime, nullable=False)
    
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    wind_speed_kmh = Column(Float, nullable=False)
    pressure_hpa = Column(Float, nullable=False)
    wind_radius_km = Column(Float, default=100.0)
    cone_radius_km = Column(Float, default=30.0)
    uncertainty_score = Column(Float, default=0.15)  # 0 to 1
    
    provenance_status = Column(String(30), default="MODELLED")
    
    cyclone = relationship("CycloneEvent", back_populates="forecasts")

class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cyclone_id = Column(String(50), ForeignKey("cyclone_events.id"), nullable=True)
    region_id = Column(String(50), nullable=True)
    
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    rainfall_1h_mm = Column(Float, default=0.0)
    rainfall_accumulated_mm = Column(Float, default=0.0)
    wind_gust_kmh = Column(Float, default=0.0)
    sea_surface_temp_c = Column(Float, default=29.5)
    tide_level_m = Column(Float, default=1.1)
    
    observed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    provenance_status = Column(String(30), default="SIMULATED")
    
    cyclone = relationship("CycloneEvent", back_populates="weather_observations")
