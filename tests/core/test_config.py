import os
import pytest
from src.utils.config import load_config, ConfigError


def test_load_config_success(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    cfg = load_config()
    assert cfg.app_env == "test"
    assert cfg.log_level == "DEBUG"


def test_load_config_missing(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    with pytest.raises(ConfigError):
        load_config()
