import hashlib
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.session import get_db
import app.models as models
from app.core.security import require_role, UserRole, TokenPayload

router = APIRouter(prefix="/advisories", tags=["Advisories & Human Approval"])

class AdvisoryApprovalRequest(BaseModel):
    action: str = "APPROVE" # APPROVE, MODIFY, REJECT
    decision_notes: Optional[str] = "Reviewed by Disaster Operations Officer"
    modifications: Optional[Dict[str, Any]] = None

@router.get("", response_model=List[Dict[str, Any]])
def list_advisories(db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).order_by(models.Alert.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "cyclone_id": a.cyclone_id,
            "region_id": a.region_id,
            "risk_level": a.risk_level,
            "title": a.title,
            "headline": a.headline,
            "advisory_text": a.advisory_text,
            "status": a.status,
            "is_official_government_warning": a.is_official_government_warning,
            "disclaimer": a.disclaimer,
            "created_at": a.created_at.isoformat()
        }
        for a in alerts
    ]

@router.post("/{advisory_id}/approve")
def approve_advisory(
    advisory_id: str,
    req: AdvisoryApprovalRequest,
    db: Session = Depends(get_db),
    user: TokenPayload = Depends(require_role([UserRole.DISASTER_MANAGER, UserRole.ADMIN, UserRole.VIEWER]))
):
    alert = db.query(models.Alert).filter_by(id=advisory_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Advisory not found")

    alert.status = "APPROVED"
    alert.is_official_government_warning = True

    # Record Human Approval entity
    approval = models.HumanApproval(
        id=f"APPR-{int(datetime.now(timezone.utc).timestamp())}",
        target_type="ADVISORY",
        target_id=advisory_id,
        action="APPROVE",
        authorized_user=user.sub or "DisasterOpsCommander",
        user_role=user.role.value,
        decision_notes=req.decision_notes,
        modifications_applied=req.modifications
    )
    db.add(approval)

    # Append to tamper-evident Audit Log
    audit_data = {
        "action": "HUMAN_APPROVAL_GRANTED",
        "advisory_id": advisory_id,
        "authorized_user": user.sub,
        "notes": req.decision_notes
    }
    raw = json.dumps(audit_data, sort_keys=True).encode("utf-8")
    checksum = hashlib.sha256(raw).hexdigest()

    db.add(models.AuditLog(
        event_type="HUMAN_APPROVAL",
        actor=user.sub or "DisasterOpsCommander",
        role=user.role.value,
        action="APPROVE_ADVISORY",
        target_entity="alerts",
        target_id=advisory_id,
        details=audit_data,
        checksum=checksum
    ))

    db.commit()
    return {
        "status": "APPROVED",
        "advisory_id": advisory_id,
        "message": "Early warning advisory approved and authorized for dissemination.",
        "audit_checksum": checksum
    }

@router.post("/{advisory_id}/reject")
def reject_advisory(
    advisory_id: str,
    req: AdvisoryApprovalRequest,
    db: Session = Depends(get_db),
    user: TokenPayload = Depends(require_role([UserRole.DISASTER_MANAGER, UserRole.ADMIN, UserRole.VIEWER]))
):
    alert = db.query(models.Alert).filter_by(id=advisory_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Advisory not found")

    alert.status = "REJECTED"

    db.add(models.HumanApproval(
        id=f"REJ-{int(datetime.now(timezone.utc).timestamp())}",
        target_type="ADVISORY",
        target_id=advisory_id,
        action="REJECT",
        authorized_user=user.sub or "DisasterOpsCommander",
        user_role=user.role.value,
        decision_notes=req.decision_notes
    ))

    audit_data = {
        "action": "HUMAN_APPROVAL_REJECTED",
        "advisory_id": advisory_id,
        "authorized_user": user.sub,
        "notes": req.decision_notes
    }
    raw = json.dumps(audit_data, sort_keys=True).encode("utf-8")
    db.add(models.AuditLog(
        event_type="HUMAN_APPROVAL",
        actor=user.sub or "DisasterOpsCommander",
        role=user.role.value,
        action="REJECT_ADVISORY",
        target_entity="alerts",
        target_id=advisory_id,
        details=audit_data,
        checksum=hashlib.sha256(raw).hexdigest()
    ))

    db.commit()
    return {"status": "REJECTED", "advisory_id": advisory_id}
