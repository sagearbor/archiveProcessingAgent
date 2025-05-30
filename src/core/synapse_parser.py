from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List


class SynapseParser:
    """Parse Azure Synapse package archives."""

    def parse_synapse_package(self, file_path: Path) -> Dict[str, Any]:
        """Categorize files and extract simple metadata."""
        contents = []
        with zipfile.ZipFile(file_path) as z:
            for name in z.namelist():
                contents.append(name)
                if name.endswith(".json"):
                    with z.open(name) as f:
                        try:
                            data = json.load(f)
                        except Exception:
                            data = None
                        if name.endswith("etl_pipeline.json"):
                            pipeline = data
                        elif name.endswith("connection_strings.json"):
                            config = data
        sql_files = [c for c in contents if c.endswith(".sql")]
        notebooks = [c for c in contents if c.endswith(".ipynb")]
        return {
            "sql_objects": self.extract_sql_objects(sql_files),
            "notebooks": self.analyze_notebooks(notebooks),
            "pipelines": locals().get("pipeline"),
            "config": locals().get("config"),
        }

    def extract_sql_objects(self, sql_files: Iterable[str]) -> List[str]:
        """Return list of SQL file names."""
        return list(sql_files)

    def analyze_notebooks(self, notebook_files: Iterable[str]) -> List[str]:
        """Return list of notebook file names."""
        return list(notebook_files)
