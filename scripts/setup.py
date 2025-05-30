from pathlib import Path
from typing import Dict, Optional
import subprocess

QUESTIONS = [
    ("AZURE_STORAGE_ACCOUNT_NAME", "Azure storage account name"),
    ("AZURE_STORAGE_ACCOUNT_KEY", "Azure storage account key"),
    ("AZURE_KEY_VAULT_URL", "Azure Key Vault URL"),
    ("APP_ENV", "Application environment"),
    ("LOG_LEVEL", "Log level"),
    ("MAX_FILE_SIZE_MB", "Maximum file size in MB"),
    ("MAX_ARCHIVE_FILES", "Maximum archive files"),
    ("TEMP_STORAGE_PATH", "Temporary storage path"),
    ("AGENT_NAME", "Agent name"),
    ("AGENT_VERSION", "Agent version"),
    ("AGENT_AUTH_TOKEN", "API key (enter MANUAL to skip)"),
]

DEFAULTS: Dict[str, str] = {}


def load_defaults(example_path: Path) -> None:
    """Load defaults from .env.example."""
    if not example_path.exists():
        return
    with example_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                DEFAULTS[key] = val


def ask(question: str, default: Optional[str] = None) -> str:
    """Prompt the user for input with optional default."""
    prompt = f"{question}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    response = input(prompt).strip()
    return response or (default or "")


def main() -> None:
    load_defaults(Path(".env.example"))
    values: Dict[str, Optional[str]] = {}

    for var, prompt in QUESTIONS[:-1]:
        values[var] = ask(prompt, DEFAULTS.get(var))

    # Last question for API key
    var, prompt = QUESTIONS[-1]
    key = ask(prompt)
    if key == "MANUAL":
        print(f'To add the API key later run:\n    echo "{var}=<your_key>" >> .env')
        values[var] = None
    else:
        values[var] = key

    with open(".env", "w", encoding="utf-8") as f:
        for var, _ in QUESTIONS:
            val = values.get(var)
            if val is not None and val != "":
                f.write(f"{var}={val}\n")

    print("\n.env configuration written.")

    run = ask("Run tests now? (y/N)", "N")
    if run.lower() in {"y", "yes"}:
        print("Running tests...\n")
        subprocess.run(["pytest", "tests/", "-q"], check=False)


if __name__ == "__main__":
    main()
