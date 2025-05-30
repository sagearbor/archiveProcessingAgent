from src.core.relevance_engine import RelevanceEngine


def test_extract_keywords():
    engine = RelevanceEngine()
    words = engine.extract_keywords("Find important code and data")
    assert words == ["find", "important", "code", "data"]


def test_score_content_relevance():
    engine = RelevanceEngine()
    score = engine.score_content_relevance("This code handles data", "find code data")
    assert score > 0.5


def test_categorize_content_and_keys():
    engine = RelevanceEngine()
    categories = engine.categorize_content(
        ["README.md", "main.py", "data.csv", "image.png"], {}
    )
    assert categories["documentation"] == ["README.md"]
    assert categories["code"] == ["main.py"]
    keys = engine.identify_key_files(categories)
    assert "README.md" in keys
    assert "main.py" in keys


def test_apply_relevance_profile():
    engine = RelevanceEngine()
    adjusted = engine.apply_relevance_profile({"code": 0.8, "documentation": 0.5}, "code_review")
    assert adjusted["code"] > adjusted["documentation"]
