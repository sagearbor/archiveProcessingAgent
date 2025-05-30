from pathlib import Path

from src.core.tableau_parser import TableauParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_twbx():
    parser = TableauParser()
    result = parser.parse_twbx(DATA_DIR / "mock_tableau.twbx")
    assert isinstance(result["dashboards"], list)
