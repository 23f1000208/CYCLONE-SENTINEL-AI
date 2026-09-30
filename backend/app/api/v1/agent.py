from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.session import get_db
from app.agents.supervisor import DisasterSupervisorAgent
from app.agents.tools import DisasterIntelligenceTools
from app.security.guardrails import PromptInjectionDefense
from app.security.output_validator import OutputValidator

router = APIRouter(prefix="/agent", tags=["AI Supervisor Agent"])

class AgentQueryRequest(BaseModel):
    query: str
    cyclone_id: Optional[str] = "CYCLONE-DEMO-01"

@router.post("/analyze")
def agent_analyze(req: AgentQueryRequest, db: Session = Depends(get_db)):
    # 1. Prompt Injection Defense
    is_safe, sanitized_query = PromptInjectionDefense.sanitize_and_validate(req.query)
    if not is_safe:
        raise HTTPException(status_code=400, detail=sanitized_query)

    # 2. Execute Supervisor Agent Bounded Tool Loop
    result = DisasterSupervisorAgent.analyze_and_respond(db, sanitized_query, req.cyclone_id or "CYCLONE-DEMO-01")

    # 3. Output & Causality Validation
    validation = OutputValidator.validate_and_filter_output(result["response"], result["structured_evidence"])
    result["response"] = validation["validated_text"]
    result["output_validation"] = {
        "passed": validation["is_valid"],
        "violations": validation["violations_detected"],
        "verified_assets": validation["cited_assets_verified"]
    }

    return result

@router.post("/response-plan")
def generate_response_plan(cyclone_id: str = "CYCLONE-DEMO-01", db: Session = Depends(get_db)):
    return DisasterIntelligenceTools.generate_response_plan(db, cyclone_id)

@router.post("/situation-report")
def generate_situation_report(cyclone_id: str = "CYCLONE-DEMO-01", db: Session = Depends(get_db)):
    return DisasterIntelligenceTools.generate_situation_report(db, cyclone_id)
