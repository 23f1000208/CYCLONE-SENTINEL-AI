from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, Text
from app.database.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)  # TOOL_CALL, SIMULATION_RUN, AGENT_REASONING, HUMAN_APPROVAL, ADVISORY_DISPATCH
    actor = Column(String(100), nullable=False)       # System, Agent, User ID
    role = Column(String(50), default="SYSTEM")
    
    action = Column(String(100), nullable=False)
    target_entity = Column(String(100), nullable=True)
    target_id = Column(String(100), nullable=True)
    
    details = Column(JSON, nullable=True)             # Full context snapshot, parameter inputs, tool outputs
    checksum = Column(String(64), nullable=True)      # SHA256 of details for tamper-evidence
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
