from pathlib import Path

import pytest

from src.core.powerbi_parser import PowerBIParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_pbix():
    parser = PowerBIParser()
    result = parser.parse_pbix(DATA_DIR / "mock_powerbi.pbix")
    assert isinstance(result["dax_measures"], list)
    assert isinstance(result["data_sources"], list)


def test_parse_corrupted_pbix(tmp_path):
    bad = tmp_path / "bad.pbix"
    bad.write_text("invalid")
    parser = PowerBIParser()
    with pytest.raises(Exception):
        parser.parse_pbix(bad)
