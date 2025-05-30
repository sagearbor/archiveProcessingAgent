from src.agent.response_formatter import ResponseFormatter


def test_format_as_executive_summary():
    formatter = ResponseFormatter()
    text = formatter.format_as_executive_summary(
        {"summary": "All good", "key_points": ["a", "b"]}, "director"
    )
    assert "Executive Summary" in text
    assert "- a" in text


def test_detect_agent_preferences():
    formatter = ResponseFormatter()
    history = [
        {"format": "json"},
        {"format": "markdown"},
        {"format": "json"},
    ]
    prefs = formatter.detect_agent_preferences({}, history)
    assert prefs["preferred_format"] == "json"


def test_customize_response_depth():
    formatter = ResponseFormatter()
    content = {"summary": "sum", "data": "info", "raw": "blob"}
    assert formatter.customize_response_depth(content, "minimal") == {"summary": "sum"}
    assert formatter.customize_response_depth(content, "detailed") == content


def test_validate_response_quality():
    formatter = ResponseFormatter()
    resp = "This report includes data summary"
    quality = formatter.validate_response_quality(resp, "data summary")
    assert quality["complete"]
