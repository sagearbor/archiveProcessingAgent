import os
from dataclasses import dataclass
from typing import Optional, Sequence

from dotenv import load_dotenv

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
except Exception:  # pragma: no cover - optional dependency
    SecretClient = None
    DefaultAzureCredential = None


class ConfigError(Exception):
    """Raised when required configuration is missing."""


@dataclass
class AppConfig:
    azure_storage_account_name: Optional[str] = None
    azure_storage_account_key: Optional[str] = None
    azure_key_vault_url: Optional[str] = None
    app_env: str = "development"
    log_level: str = "INFO"
    max_file_size_mb: int = 100
    temp_storage_path: str = "/tmp/archive_processing"
    agent_name: str = "archive-processing-agent"
    agent_version: str = "1.0.0"
    agent_auth_token: Optional[str] = None


REQUIRED_VARS: Sequence[str] = ("APP_ENV", "LOG_LEVEL")


def _load_from_key_vault(vault_url: str) -> None:
    """Load secrets from Azure Key Vault into environment variables."""
    if SecretClient is None or DefaultAzureCredential is None:
        return
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        for var in REQUIRED_VARS:
            if os.getenv(var) is None:
                try:
                    secret = client.get_secret(var)
                    os.environ[var] = secret.value
                except Exception:
                    pass
    except Exception:
        pass


def _validate_required_vars() -> None:
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            raise ConfigError(f"Missing required configuration variable: {var}")


def load_config() -> AppConfig:
    """Load application configuration with optional Key Vault support."""
    load_dotenv()
    vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    if vault_url:
        _load_from_key_vault(vault_url)

    _validate_required_vars()

    return AppConfig(
        azure_storage_account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME"),
        azure_storage_account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY"),
        azure_key_vault_url=vault_url,
        app_env=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "100")),
        temp_storage_path=os.getenv("TEMP_STORAGE_PATH", "/tmp/archive_processing"),
        agent_name=os.getenv("AGENT_NAME", "archive-processing-agent"),
        agent_version=os.getenv("AGENT_VERSION", "1.0.0"),
        agent_auth_token=os.getenv("AGENT_AUTH_TOKEN"),
    )


class ConfigManager:
    """Provides access to application configuration values."""

    def __init__(self) -> None:
        self._config = load_config()

    def get_azure_storage_config(self) -> dict:
        """Return Azure Storage connection configuration."""
        return {
            "account_name": self._config.azure_storage_account_name,
            "account_key": self._config.azure_storage_account_key,
            "key_vault_url": self._config.azure_key_vault_url,
        }

    def get_application_config(self) -> AppConfig:
        """Return loaded application configuration dataclass."""
        return self._config
