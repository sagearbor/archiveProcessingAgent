from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List


class TableauParser:
    """Parse Tableau .twbx files."""

    def parse_twbx(self, file_path: Path) -> Dict[str, Any]:
        """Extract basic information from a TWBX file."""
        with zipfile.ZipFile(file_path) as z:
            workbook_xml = None
            if "workbook.xml" in z.namelist():
                with z.open("workbook.xml") as f:
                    workbook_xml = ET.parse(f)

            workbook_data: Dict[str, Any] = {}
            if workbook_xml is not None:
                root = workbook_xml.getroot()
                workbook_data["datasources"] = [
                    ds.get("name") for ds in root.findall(".//datasource")
                ]
                workbook_data["worksheets"] = [
                    ws.get("name") for ws in root.findall(".//worksheet")
                ]

            return {
                "calculated_fields": self.extract_calculated_fields(workbook_data),
                "dashboards": self.get_dashboards_info(workbook_data),
            }

    def extract_calculated_fields(self, workbook_data: Dict[str, Any]) -> List[str]:
        """Return calculated field names if present."""
        return workbook_data.get("calculated_fields", [])

    def get_dashboards_info(self, workbook_data: Dict[str, Any]) -> List[str]:
        """Return dashboard names if present."""
        return workbook_data.get("dashboards", workbook_data.get("worksheets", []))
