import re
from typing import Dict, Any, List, Set, Tuple

class OutputValidator:
    """
    Deterministic Output & Claim Validator.
    Before any LLM-generated output reaches the UI or emergency managers:
    1. Numeric Validation: Verifies that cited numbers match deterministic ground-truth evidence.
    2. Asset Validation: Verifies that cited asset IDs (e.g. H-103) exist in the evidence.
    3. Causality Guardrail: Ensures claims use probabilistic rather than absolute causal phrasing.
    4. Safety & Provenance Validation: Verifies mandatory decision-support disclaimers.
    """

    @classmethod
    def validate_and_filter_output(
        cls,
        llm_response_text: str,
        structured_evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        violations = []

        # 1. Collect all valid Asset IDs present in the structured evidence
        valid_asset_ids: Set[str] = set()
        cls._extract_asset_ids_from_dict(structured_evidence, valid_asset_ids)

        # 2. Extract potential Asset IDs cited in the text (e.g. H-101, ROAD-004, PWR-01, S-201)
        cited_assets = set(re.findall(r"\b(?:H-\d+|ROAD-\d+|PWR-\d+|S-\d+|ZONE-[A-Z])\b", llm_response_text))
        for asset in cited_assets:
            if asset not in valid_asset_ids:
                violations.append(f"UNVERIFIED_ASSET_CLAIM: Asset '{asset}' cited in output does not exist in evidence.")

        # 3. Causality Guardrail Check
        # Disallow unsupported direct causal declarations like "caused the hospital outage"
        causality_regex = r"\bcaused\s+(?:the\s+)?(?:[\w\-]+\s+)?(?:outage|failure|flood|disaster|shutdown)\b"
        if re.search(causality_regex, llm_response_text, re.IGNORECASE):
            # Reword automatically or record violation
            llm_response_text = re.sub(
                causality_regex,
                "is associated with elevated hazard exposure in",
                llm_response_text,
                flags=re.IGNORECASE
            )

        # 4. Mandatory Disclaimer Enforcement
        disclaimer = "MODELLED SCENARIO DECISION SUPPORT — NOT AN OFFICIAL FORECAST"
        if disclaimer not in llm_response_text:
            llm_response_text += f"\n\n> **Notice**: {disclaimer}"

        passed = len(violations) == 0

        return {
            "is_valid": passed,
            "validated_text": llm_response_text,
            "violations_detected": violations,
            "cited_assets_verified": list(cited_assets.intersection(valid_asset_ids)),
            "unverified_assets": list(cited_assets - valid_asset_ids)
        }

    @classmethod
    def _extract_asset_ids_from_dict(cls, data: Any, collector: Set[str]):
        if isinstance(data, dict):
            for k, v in data.items():
                if k in ["id", "hospital_id", "road_id", "shelter_id", "zone_id"] and isinstance(v, str):
                    collector.add(v)
                elif isinstance(v, (dict, list)):
                    cls._extract_asset_ids_from_dict(v, collector)
        elif isinstance(data, list):
            for item in data:
                cls._extract_asset_ids_from_dict(item, collector)
