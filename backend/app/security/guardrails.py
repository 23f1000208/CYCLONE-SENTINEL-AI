import re
from typing import Dict, Any, List, Tuple

class PromptInjectionDefense:
    """
    Defends against adversarial prompt injection attempts in incoming user text.
    Rejects unauthorized override instructions before any tool or agent execution.
    """
    FORBIDDEN_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"reveal\s+(your\s+)?(api[_\s]?key|secret|password)",
        r"change\s+(the\s+)?risk\s+score",
        r"send\s+(this\s+)?warning\s+automatically",
        r"bypass\s+(human\s+)?approval",
        r"execute\s+arbitrary\s+sql",
        r"drop\s+table",
    ]

    @classmethod
    def sanitize_and_validate(cls, user_text: str) -> Tuple[bool, str]:
        text_lower = user_text.lower()
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, text_lower):
                return False, f"Input rejected by Security Guardrail: matched forbidden instruction pattern '{pattern}'"
        return True, user_text.strip()
