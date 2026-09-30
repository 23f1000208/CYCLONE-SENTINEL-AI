from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey, Text
from app.database.session import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(50), primary_key=True, index=True)
    cyclone_id = Column(String(50), ForeignKey("cyclone_events.id"), nullable=False)
    region_id = Column(String(50), ForeignKey("geographic_regions.id"), nullable=False)
    
    risk_level = Column(String(20), nullable=False)  # GREEN (Monitoring), YELLOW (Preparedness), ORANGE (Enhanced), RED (Emergency)
    title = Column(String(200), nullable=False)
    headline = Column(String(300), nullable=False)
    advisory_text = Column(Text, nullable=False)
    
    # State flags
    status = Column(String(30), default="DRAFT")  # DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, SUPERSEDED
    is_official_government_warning = Column(Boolean, default=False)
    disclaimer = Column(String(250), default="MODELLED EARLY WARNING ADVISORY — REQUIRES AUTHORIZED HUMAN CONFIRMATION")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(String(50), primary_key=True, index=True)
    cyclone_id = Column(String(50), ForeignKey("cyclone_events.id"), nullable=False)
    category = Column(String(50), nullable=False)  # EVACUATION_ROUTING, HOSPITAL_RESOURCES, SHELTER_ALLOCATION, POWER_ISOLATION
    
    title = Column(String(200), nullable=False)
    action_summary = Column(Text, nullable=False)
    priority = Column(String(20), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    
    # Structured evidence grounding
    grounding_evidence = Column(JSON, nullable=False)
    model_confidence = Column(Float, default=0.92)
    uncertainty_notes = Column(Text, nullable=True)
    
    approval_status = Column(String(30), default="PENDING_REVIEW")  # PENDING_REVIEW, APPROVED, MODIFIED, REJECTED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class HumanApproval(Base):
    __tablename__ = "human_approvals"

    id = Column(String(50), primary_key=True, index=True)
    target_type = Column(String(50), nullable=False)  # ADVISORY, RECOMMENDATION, SIMULATION_ACTION
    target_id = Column(String(50), nullable=False)
    
    action = Column(String(30), nullable=False)  # APPROVE, MODIFY, REJECT
    authorized_user = Column(String(100), nullable=False)
    user_role = Column(String(50), nullable=False)  # DISASTER_MANAGER, ADMIN
    
    decision_notes = Column(Text, nullable=True)
    modifications_applied = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
