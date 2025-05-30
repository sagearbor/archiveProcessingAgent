import pytest
from pathlib import Path
from src.agent.archive_agent import ArchiveAgent
from src.agent.authentication import TokenAuthenticator

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_unauthorized_request():
    auth = TokenAuthenticator(valid_tokens=["secret"])
    agent = ArchiveAgent(authenticator=auth)
    with pytest.raises(PermissionError):
        agent.process_request(
            str(DATA_DIR / "mock_word.docx"), "extract", auth_token="wrong"
        )


def test_file_not_found():
    agent = ArchiveAgent()
    with pytest.raises(FileNotFoundError):
        agent.process_request("/no/such/file.zip", "list", auth_token=None)


def test_unsupported_file(tmp_path):
    file = tmp_path / "data.xyz"
    file.write_text("data")
    agent = ArchiveAgent()
    result = agent.process_request(str(file), "analyze")
    assert result["content"] == {"unsupported": str(file)}
