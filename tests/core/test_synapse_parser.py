from pathlib import Path

from src.core.synapse_parser import SynapseParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_synapse_package():
    parser = SynapseParser()
    result = parser.parse_synapse_package(DATA_DIR / "mock_synapse.zip")
    assert "sql_objects" in result
    assert "notebooks" in result
