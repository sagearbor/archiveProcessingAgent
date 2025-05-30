from pathlib import Path

from src.core.powerbi_parser import PowerBIParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_pbix():
    parser = PowerBIParser()
    result = parser.parse_pbix(DATA_DIR / "mock_powerbi.pbix")
    assert isinstance(result["dax_measures"], list)
    assert isinstance(result["data_sources"], list)
