from src.agent.request_interpreter import RequestInterpreter


def test_analyze_intent_extract():
    interpreter = RequestInterpreter()
    res = interpreter.analyze_request_intent("Please extract the data")
    assert res["intent"] == "extract"
    assert "data" in res["keywords"]


def test_extract_request_parameters():
    interpreter = RequestInterpreter()
    analysis = interpreter.analyze_request_intent("Summarize the document")
    params = interpreter.extract_request_parameters("Summarize the document", analysis)
    assert params["keywords"]
