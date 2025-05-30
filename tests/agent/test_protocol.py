from src.agent.protocol import AgentRequest, AgentResponse


def test_agent_request_to_dict():
    req = AgentRequest(file_path="file.zip", request_text="extract")
    data = req.to_dict()
    assert data["file_path"] == "file.zip"
    assert data["request_text"] == "extract"
    assert data["response_format"] == "markdown"
    assert data["agent"] == "unknown"
    assert data["metadata"] == {}


def test_agent_response_to_dict():
    resp = AgentResponse(status="success", message="ok", data={"a": 1})
    data = resp.to_dict()
    assert data["status"] == "success"
    assert data["message"] == "ok"
    assert data["data"] == {"a": 1}
    assert data["metadata"] == {}
