# Scripts

Helper utilities for configuration and deployment.

- `setup.py` - interactive CLI to create `.env` and optionally run tests.
- `setup.html` - browser-based form for generating `.env`.
- `build_setup_html.py` - regenerate `setup.html` if it's missing or outdated.
  Automatically chooses a Windows or Unix default for `TEMP_STORAGE_PATH`.
