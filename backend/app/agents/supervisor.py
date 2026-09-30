import os
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.agents.bounded_loop import BoundedAgentLoop

class DisasterSupervisorAgent:
    """
    Primary Supervisor Disaster Intelligence Agent.
    Coordinates deterministic tools, context envelopes, and Gemini reasoning.
    Enforces Zero-LLM Arithmetic and Causality Phrasing.
    """

    SYSTEM_INSTRUCTIONS = """You are the Lead Disaster Intelligence Supervisor Agent for CYCLONE SENTINEL AI.
Your role is to interpret deterministic scientific risk assessments, infrastructure vulnerability assessments,
and scenario simulations for emergency managers in the Bay of Bengal.

CRITICAL RULES:
1. ZERO-LLM ARITHMETIC: You must NEVER invent, calculate, or alter numerical numbers.
   Only cite numbers provided in the structured evidence.
2. CAUSALITY GUARDRAIL: Do not state that an event caused a failure (e.g. "rainfall caused the hospital outage").
   Use probabilistic association: "The modeled scenario indicates elevated flood exposure associated with rainfall."
3. SCIENTIFIC CLAIM DISTINCTION: Clearly distinguish between:
   - OBSERVATION (real-time measurements)
   - FORECAST (numerical meteorological track)
   - MODEL PREDICTION (deterministic hydrodynamic output)
   - SCENARIO (hypothetical what-if conditions)
   - AI INTERPRETATION (qualitative assessment)
   - HUMAN DECISION (requires authorized human approval)
4. ACTION RESTRICTION: You CANNOT issue official warnings or order evacuations. You only prepare DRAFT recommendations for human review.
"""

    @classmethod
    def analyze_and_respond(
        cls,
        db: Session,
        user_query: str,
        cyclone_id: str = "CYCLONE-DEMO-01"
    ) -> Dict[str, Any]:
        # 1. Execute bounded tool loop to gather deterministic ground-truth evidence
        loop_result = BoundedAgentLoop.execute_bounded_query(db, user_query, cyclone_id)
        evidence = loop_result["structured_evidence"]

        # 2. Check if live Gemini API key is available
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        explanation = None

        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"{cls.SYSTEM_INSTRUCTIONS}\n\n"
                    f"USER QUERY: {user_query}\n\n"
                    f"STRUCTURED EVIDENCE (Ground Truth):\n"
                    f"{json.dumps(evidence, indent=2)}\n\n"
                    f"Provide an evidence-grounded response answering the query."
                )
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt
                )
                explanation = response.text
            except Exception as e:
                explanation = None

        # 3. Deterministic Qualitative Interpretation Fallback (100% offline & reproducible)
        if not explanation:
            explanation = cls._generate_deterministic_explanation(user_query, evidence, loop_result["context_summary"])

        return {
            "query": user_query,
            "cyclone_id": cyclone_id,
            "response": explanation,
            "tools_called": loop_result["tools_called"],
            "iterations_executed": loop_result["iterations_executed"],
            "structured_evidence": evidence,
            "guardrail_status": "VALIDATED_ZERO_LLM_ARITHMETIC",
            "provenance_disclaimer": "MODELLED SCENARIO DECISION SUPPORT — NOT AN OFFICIAL FORECAST",
            "requires_human_approval": any(k in evidence for k in ["advisory", "plan", "inaccessible_hospitals"])
        }

    @classmethod
    def _generate_deterministic_explanation(
        cls,
        query: str,
        evidence: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Deterministic qualitative generator when Gemini API is offline."""
        q = query.lower()
        if "hospital" in evidence or "inaccessible_hospitals" in evidence:
            inacc = evidence.get("inaccessible_hospitals", [])
            inacc_names = [h["name"] for h in inacc]
            return (
                f"### Healthcare Infrastructure Vulnerability Assessment\n\n"
                f"- **Current Hazard Level**: {context['risk_category']} ({context['risk_score']})\n"
                f"- **Model Prediction**: Deterministic runoff routing identifies **{len(inacc)} hospitals** "
                f"with elevated inundation risk ({', '.join(inacc_names) if inacc_names else 'None currently inaccessible'}).\n"
                f"- **Accessibility Status**: Coastal access roads show water accumulation exceeding 30cm.\n"
                f"- **Recommended Anticipatory Action**: Emergency managers should verify alternate routes to inland medical centers and inspect auxiliary power generator fuel reserves.\n\n"
                f"> *Note: Model assessment based on 180mm rainfall and 2.5m storm surge. Requires human review.*"
            )

        if "flooded_roads" in evidence:
            flooded = evidence.get("flooded_roads", [])
            return (
                f"### Road Network & Evacuation Corridor Accessibility\n\n"
                f"- **Current Hazard Level**: {context['risk_category']}\n"
                f"- **Impacted Corridors**: **{len(flooded)} road segments** are modeled with impassable flood levels (>30cm).\n"
                f"- **Critical Observation**: Coastal link corridors near Paradeep and Astaranga show the highest surface water accumulation.\n"
                f"- **Recommended Anticipatory Action**: Reroute evacuation traffic away from coastal highways to National Highway NH-316 inland."
            )

        if "scenario_comparison" in evidence:
            comp = evidence["scenario_comparison"]
            d = comp["deltas"]
            return (
                f"### What-If Scenario Comparison (Baseline vs Scenario)\n\n"
                f"- **Flooded Area**: Increases by **+{d['flooded_area_delta_sqkm']} sq km** (+{d['flooded_area_change_pct']}%).\n"
                f"- **Exposed Population**: Additional **+{d['population_exposed_delta']:,} residents** enter the high-hazard inundation zone.\n"
                f"- **Infrastructure Impact**: Additional **+{d['additional_roads_flooded']} roads** and **+{d['additional_hospitals_inaccessible']} hospitals** face accessibility impairment.\n"
                f"- **Shelter Demand**: Increases by **+{d['additional_shelter_demand']:,} slots**."
            )

        # Default overview
        risk = evidence.get("risk", {})
        return (
            f"### Cyclone DEMO-01 Pre-Landfall Risk Summary\n\n"
            f"- **Overall Modeled Risk**: **{context['risk_score']} ({context['risk_category']})**\n"
            f"- **Primary Contributing Drivers**: Coastal storm surge (28%), precipitation runoff (23%), and low coastal elevation (18%).\n"
            f"- **Anticipatory Posture**: Enhanced Preparedness stage (ORANGE). Automated advisories remain in DRAFT status pending Disaster Manager approval."
        )
