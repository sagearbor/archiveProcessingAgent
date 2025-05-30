from pathlib import Path

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
