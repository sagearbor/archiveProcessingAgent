from pathlib import Path

import pytest

from src.core.tableau_parser import TableauParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_twbx():
    parser = TableauParser()
    result = parser.parse_twbx(DATA_DIR / "mock_tableau.twbx")
    assert isinstance(result["dashboards"], list)


def test_parse_corrupted_twbx(tmp_path):
    bad = tmp_path / "bad.twbx"
    bad.write_text("invalid")
    parser = TableauParser()
    with pytest.raises(Exception):
        parser.parse_twbx(bad)
