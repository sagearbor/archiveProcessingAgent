from __future__ import annotations

import re
from typing import Dict, List


class RequestInterpreter:
    """Very small helper class to analyze request text."""

    STOPWORDS = {"the", "and", "is", "a", "an", "of", "for", "to"}

    def analyze_request_intent(self, request_text: str) -> Dict[str, str]:
        text = request_text.lower()
        if "summarize" in text or "summary" in text:
            intent = "summarize"
        elif "extract" in text:
            intent = "extract"
        elif "list" in text:
            intent = "list"
        else:
            intent = "analyze"
        keywords = self._extract_keywords(text)
        return {"intent": intent, "keywords": keywords}

    def extract_request_parameters(
        self, request_text: str, intent_analysis: Dict[str, str]
    ) -> Dict[str, List[str]]:
        return {"keywords": intent_analysis.get("keywords", [])}

    def _extract_keywords(self, text: str) -> List[str]:
        tokens = re.findall(r"[A-Za-z0-9_]+", text)
        return [t for t in tokens if t not in self.STOPWORDS]
