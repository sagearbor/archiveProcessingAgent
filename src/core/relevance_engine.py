from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


class RelevanceEngine:
    """Simple relevance scoring and content categorization."""

    STOPWORDS = {"the", "and", "is", "a", "an", "of", "for", "to"}

    def extract_keywords(self, request_text: str) -> List[str]:
        """Return significant lowercase keywords from the request."""
        tokens = re.findall(r"[A-Za-z0-9_]+", request_text.lower())
        return [t for t in tokens if t not in self.STOPWORDS]

    def match_content_to_intent(
        self, content: str, intent_keywords: Sequence[str]
    ) -> float:
        """Return ratio of intent keywords found in content."""
        if not intent_keywords:
            return 0.0
        text = content.lower()
        matches = sum(1 for kw in intent_keywords if kw in text)
        return matches / len(intent_keywords)

    def score_content_relevance(self, content: str, request_context: str) -> float:
        """Score content relevance to request context on 0..1 scale."""
        keywords = self.extract_keywords(request_context)
        return self.match_content_to_intent(content, keywords)

    def categorize_content(
        self, file_list: Iterable[str], content_data: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """Categorize files by simple extension rules."""
        categories: Dict[str, List[str]] = defaultdict(list)
        for file in file_list:
            ext = Path(file).suffix.lower()
            if ext in {".csv", ".json", ".xlsx"}:
                categories["data"].append(file)
            elif ext in {".py", ".js", ".java"}:
                categories["code"].append(file)
            elif ext in {".md", ".txt", ".docx"}:
                categories["documentation"].append(file)
            elif ext in {".ini", ".cfg", ".yaml", ".yml"}:
                categories["configuration"].append(file)
            elif ext in {".png", ".jpg", ".jpeg"}:
                categories["media"].append(file)
            else:
                categories["other"].append(file)
        return dict(categories)

    def identify_key_files(self, categorized_content: Dict[str, List[str]]) -> List[str]:
        """Return key files such as READMEs or main modules."""
        key_files: List[str] = []
        for files in categorized_content.values():
            for f in files:
                lower = f.lower()
                if "readme" in lower or "main" in lower:
                    key_files.append(f)
        if not key_files:
            for cat in ["documentation", "code", "data"]:
                files = categorized_content.get(cat, [])
                if files:
                    key_files.append(files[0])
        return key_files

    def apply_relevance_profile(
        self, scores: Dict[str, float], profile_name: str
    ) -> Dict[str, float]:
        """Adjust scores using profile-specific weights."""
        weights = {
            "data_analysis": {"data": 1.0, "documentation": 0.6, "code": 0.4},
            "code_review": {"code": 1.0, "tests": 0.8, "documentation": 0.2},
            "business_intelligence": {"data": 0.7, "documentation": 0.5, "code": 0.2},
            "documentation": {"documentation": 1.0, "code": 0.3, "data": 0.3},
            "configuration": {"configuration": 1.0, "code": 0.2, "documentation": 0.4},
        }
        profile = weights.get(profile_name, {})
        adjusted = {}
        for name, score in scores.items():
            weight = profile.get(name, 1.0)
            adjusted[name] = score * weight
        return adjusted
