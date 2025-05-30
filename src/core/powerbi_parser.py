from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any, Dict, List


class PowerBIParser:
    """Parse Power BI .pbix files."""

    def parse_pbix(self, file_path: Path) -> Dict[str, Any]:
        """Extract basic information from a PBIX file."""
        with zipfile.ZipFile(file_path) as z:
            model_data = {}
            if "DataModel/model.bim" in z.namelist():
                with z.open("DataModel/model.bim") as f:
                    model_data = json.load(f)

            report_data = {}
            if "Report/report.json" in z.namelist():
                with z.open("Report/report.json") as f:
                    report_data = json.load(f)

            return {
                "dax_measures": self.extract_dax_measures(model_data),
                "data_sources": self.get_data_sources(model_data),
                "visualizations": report_data.get("visuals", []),
            }

    def extract_dax_measures(self, model_data: Dict[str, Any]) -> List[str]:
        """Return a list of DAX measure expressions."""
        measures = []
        for table in model_data.get("tables", []):
            for measure in table.get("measures", []):
                expression = measure.get("expression")
                if expression:
                    measures.append(expression)
        return measures

    def get_data_sources(self, model_data: Dict[str, Any]) -> List[str]:
        """Return data source connection strings."""
        sources = []
        for ds in model_data.get("dataSources", []):
            conn = ds.get("connectionString")
            if conn:
                sources.append(conn)
        return sources
