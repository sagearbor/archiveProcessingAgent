from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.archive_handler import ArchiveHandler
from src.core.office_parser import OfficeParser
from src.core.powerbi_parser import PowerBIParser
from src.core.tableau_parser import TableauParser
from src.core.synapse_parser import SynapseParser
from src.core.relevance_engine import RelevanceEngine
from src.core.content_summarizer import ContentSummarizer
from src.utils.config import load_config
from .authentication import TokenAuthenticator

from .request_interpreter import RequestInterpreter


class ArchiveAgent:
    """Main agent class orchestrating archive processing."""

    def __init__(self, authenticator: TokenAuthenticator | None = None) -> None:
        self.config = load_config()
        self.archive_handler = ArchiveHandler()
        self.office_parser = OfficeParser()
        self.powerbi_parser = PowerBIParser()
        self.tableau_parser = TableauParser()
        self.synapse_parser = SynapseParser()
        self.relevance_engine = RelevanceEngine()
        self.summarizer = ContentSummarizer()
        self.interpreter = RequestInterpreter()
        self.authenticator = authenticator or TokenAuthenticator()
        self.context: List[Dict[str, Any]] = []

    def process_request(
        self,
        file_path: str,
        request_text: str,
        context: Optional[Dict[str, Any]] = None,
        auth_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a request against the provided file."""
        if not self.authenticator.is_authorized(auth_token):
            raise PermissionError("Unauthorized")

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(file_path)

        intent = self.interpreter.analyze_request_intent(request_text)
        params = self.interpreter.extract_request_parameters(request_text, intent)
        strategy = self.determine_processing_strategy(path, intent)
        content = self.route_to_appropriate_parser(path, strategy["type"], intent)

        summary = self.summarizer.generate_executive_summary(
            {"files": [str(path)], "categories": {"files": [str(path)]}},
            request_text,
        )
        response = {"summary": summary, "content": content, "parameters": params}
        self.context.append({"request": request_text, "response": response})
        return response

    def determine_processing_strategy(
        self, file_path: Path, intent_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        ext = file_path.suffix.lower()
        if ext in {".docx", ".xlsx", ".pptx"}:
            file_type = "office"
        elif ext == ".pbix":
            file_type = "powerbi"
        elif ext == ".twbx":
            file_type = "tableau"
        elif ext == ".zip" and file_path.name.endswith("synapse.zip"):
            file_type = "synapse"
        else:
            detected = self.archive_handler.detect_archive_type(file_path)
            file_type = detected or "unknown"
        return {"type": file_type, "intent": intent_analysis.get("intent")}

    def route_to_appropriate_parser(
        self, file_path: Path, file_type: str, intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        if file_type == "office":
            if file_path.suffix.lower() == ".docx":
                return self.office_parser.parse_docx(file_path)
            if file_path.suffix.lower() == ".xlsx":
                return self.office_parser.parse_xlsx(file_path)
            if file_path.suffix.lower() == ".pptx":
                return self.office_parser.parse_pptx(file_path)
        if file_type == "powerbi":
            return self.powerbi_parser.parse_pbix(file_path)
        if file_type == "tableau":
            return self.tableau_parser.parse_twbx(file_path)
        if file_type == "synapse":
            return self.synapse_parser.parse_synapse_package(file_path)
        if file_type in {"zip", "tar", "7z"}:
            files = self.archive_handler.list_contents(file_path)
            return {"files": files}
        return {"unsupported": str(file_path)}
