import os
import pytest
from src.utils.config import load_config, ConfigError, ConfigManager


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


def test_config_manager(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("STORAGE_PROVIDER", "azure")
    monkeypatch.setenv("STORAGE_ACCOUNT_NAME", "acc")
    monkeypatch.setenv("STORAGE_ACCOUNT_KEY", "key")
    mgr = ConfigManager()
    storage_cfg = mgr.get_storage_config()
    assert storage_cfg["account_name"] == "acc"
    app_cfg = mgr.get_application_config()
    assert app_cfg.app_env == "test"
