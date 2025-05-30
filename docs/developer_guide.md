# Developer Guide

This guide describes the project architecture and development workflow.

## Architecture Overview
The code is organized under the `src` directory with submodules for core utilities, the MCP tool and the A2A agent.

## Contributing
- Ensure new features include unit tests.
- Run `pytest` before committing.
- Follow the coding standards documented in `AGENTS.md`.

## Release Process
Packages are built from `pyproject.toml` using `python -m build` and can be published to an internal repository or PyPI.
