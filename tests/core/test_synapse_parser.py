from pathlib import Path
import zipfile

import pytest

from src.core.synapse_parser import SynapseParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_synapse_package():
    parser = SynapseParser()
    result = parser.parse_synapse_package(DATA_DIR / "mock_synapse.zip")
    assert "sql_objects" in result
    assert "notebooks" in result


def test_parse_corrupted_synapse(tmp_path):
    bad = tmp_path / "bad.zip"
    bad.write_text("invalid")
    parser = SynapseParser()
    with pytest.raises(Exception):
        parser.parse_synapse_package(bad)


def test_synapse_parsing_accuracy(tmp_path):
    archive = tmp_path / "synapse.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("scripts/create.sql", "CREATE TABLE t(id INT);")
        z.writestr("notebooks/analysis.ipynb", "{}")
        z.writestr("pipelines/etl_pipeline.json", "{}")
        z.writestr("config/connection_strings.json", '{"conn": "val"}')

    parser = SynapseParser()
    result = parser.parse_synapse_package(archive)
    assert result["sql_objects"] == ["scripts/create.sql"]
    assert result["notebooks"] == ["notebooks/analysis.ipynb"]
    assert result["pipelines"] == {}
    assert result["config"] == {"conn": "val"}


def test_synapse_malformed_json(tmp_path):
    archive = tmp_path / "synapse_bad.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("pipelines/etl_pipeline.json", "{ bad json }")

    parser = SynapseParser()
    result = parser.parse_synapse_package(archive)
    assert result["pipelines"] is None


def test_synapse_empty_package(tmp_path):
    archive = tmp_path / "empty.zip"
    with zipfile.ZipFile(archive, "w"):
        pass

    parser = SynapseParser()
    result = parser.parse_synapse_package(archive)
    assert result["sql_objects"] == []
    assert result["notebooks"] == []
    assert result["pipelines"] is None
    assert result["config"] is None
