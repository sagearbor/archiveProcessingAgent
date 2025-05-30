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

## Error Codes

| Message | Meaning | Suggested Resolution |
|---------|---------|----------------------|
| `File not found` | The provided path does not exist | Verify the file path |
| `Invalid extraction mode` | Unsupported mode name | Use one of `basic`, `detailed`, `content`, `smart` |
| `Unsupported archive type` | File is not a recognized archive | Check the file extension and format |
| `Permission denied. Check file permissions and try again.` | Process lacks permissions | Adjust file permissions |
| `Corrupted archive file. Unable to extract.` | Archive is damaged or unreadable | Replace or recreate the archive |
| `Out of disk space during extraction. Free space and retry.` | Temporary directory ran out of space | Free disk space or set `TEMP_STORAGE_PATH` |
