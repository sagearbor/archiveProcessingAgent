# MCP Tool Usage

The `extract_archive_tool` provides a simple interface for extracting archives.

## Parameters
- `file_path` *(str)*: Path to the archive file.
- `extraction_mode` *(str)*: Extraction mode, default `"basic"`.
- `include_metadata` *(bool)*: Include processing metadata.
- `max_files` *(int)*: Limit number of returned files.

## Example
```python
from src.mcp.mcp_tool import extract_archive_tool
result = extract_archive_tool("mock_data/mock_archive.zip")
```
