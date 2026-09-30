from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
import app.models as models

router = APIRouter(prefix="/audit", tags=["Compliance & Audit Logs"])

@router.get("", response_model=List[Dict[str, Any]])
def get_audit_trail(db: Session = Depends(get_db)):
    logs = db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(100).all()
    return [
        {
            "id": log.id,
            "event_type": log.event_type,
            "actor": log.actor,
            "role": log.role,
            "action": log.action,
            "target_entity": log.target_entity,
            "target_id": log.target_id,
            "details": log.details,
            "checksum": log.checksum,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]
