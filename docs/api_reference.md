# API Reference

This document provides a high level overview of the main classes and functions available in the archive processing agent.

## `src.core.archive_handler.ArchiveHandler`
- `detect_archive_type(path)`: Return the archive type based on extension.
- `extract_archive(path, extract_to=None, max_members=1000)`: Extract an archive to a folder.
- `list_contents(path)`: List files without extraction.
- `temp_extract(path, max_members=1000)`: Context manager that extracts to a temporary directory and cleans up when done.

## `src.core.office_parser.OfficeParser`
Parsers for Word, Excel and PowerPoint documents. Key methods include `parse_docx`, `parse_xlsx` and `parse_pptx` which return structured dictionaries.

## `src.agent.archive_agent.ArchiveAgent`
High level agent interface that routes requests and returns structured responses.

Refer to the source files for complete parameter details and return types.
