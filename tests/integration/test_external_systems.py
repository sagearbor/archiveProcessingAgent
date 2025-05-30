import pytest
from src.utils import config

class FakeSecret:
    def __init__(self, value):
        self.value = value

class FakeSecretClient:
    def __init__(self, vault_url, credential):
        self.vault_url = vault_url
        self.credential = credential

    def get_secret(self, name):
        data = {"APP_ENV": "prod", "LOG_LEVEL": "WARNING"}
        return FakeSecret(data.get(name))

class FakeCredential:
    pass


def test_load_config_from_key_vault(monkeypatch):
    monkeypatch.setenv("AZURE_KEY_VAULT_URL", "https://vault")
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.setattr(config, "SecretClient", FakeSecretClient)
    monkeypatch.setattr(config, "DefaultAzureCredential", FakeCredential)
    cfg = config.load_config()
    assert cfg.app_env == "prod"
    assert cfg.log_level == "WARNING"
