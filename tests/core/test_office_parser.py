from pathlib import Path

from src.core.office_parser import OfficeParser

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_parse_docx():
    parser = OfficeParser()
    result = parser.parse_docx(DATA_DIR / "mock_word.docx")
    assert "Test Document" in result["headings"][0]
    paragraph_texts = [p["text"] for p in result["paragraphs"]]
    assert "This is a test paragraph." in paragraph_texts
    assert "tables" in result
    assert result["metadata"]["author"] == "tester"


def test_parse_xlsx():
    parser = OfficeParser()
    result = parser.parse_xlsx(DATA_DIR / "mock_excel.xlsx")
    assert "Sheet1" in result["sheets"]
    assert result["sheets"]["Sheet1"]["data"][0][0] == "data"


def test_parse_pptx():
    parser = OfficeParser()
    result = parser.parse_pptx(DATA_DIR / "mock_powerpoint.pptx")
    assert any("Title" in slide["texts"][0] for slide in result["slides"])
