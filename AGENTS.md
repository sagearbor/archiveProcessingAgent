# AGENTS.md - Archive Processing Agent Instructions

## Project Overview
This project creates an A2A agent that can intelligently extract and process various archive formats (ZIP, TAR, Word, PowerBI, Tableau, Synapse) and return relevant content to other agents.

## Development Approach
- **Code one step at a time** - Complete each step fully before moving to the next
- **Test with mock data** - Each step should work completely offline  
- **Modular design** - Each component should be independently testable
- **Follow the checklist** - Work through each phase systematically

## Project Architecture
```
A2A Archive Agent
├── Core Python Libraries (reusable utilities)
│   ├── archive_handler.py      # Basic ZIP/TAR extraction
│   ├── office_parser.py        # Word/Excel/PowerPoint processing
│   ├── powerbi_parser.py       # Power BI file structure parsing
│   ├── tableau_parser.py       # Tableau workbook processing
│   ├── synapse_parser.py       # Azure Synapse package handling
│   ├── relevance_engine.py     # Content filtering and scoring
│   └── content_summarizer.py   # Intelligent summarization
├── MCP Tool Interface (for simple operations)
│   └── mcp_tool.py             # Direct tool calls for basic extraction
└── A2A Agent Layer (for complex processing)
    ├── archive_agent.py        # Main agent logic and conversation handling
    ├── request_interpreter.py  # Natural language request parsing
    └── response_formatter.py   # Adaptive output formatting
```

## Code Style & Standards
- Use Python 3.8+ with type hints
- Follow PEP 8 formatting with Black formatter
- Use descriptive variable names (no abbreviations)
- Add comprehensive docstrings for all functions and classes
- Use pathlib for file operations
- Handle errors gracefully with informative messages

## Required Libraries
```python
# Core
zipfile, tarfile, tempfile, pathlib, json, logging

# Office documents  
python-docx, openpyxl, python-pptx

# Archive handling
py7zr, rarfile (optional)

# XML/parsing
xml.etree.ElementTree, lxml

# Testing
pytest, unittest.mock
```

## Directory Structure
```
/
├── src/
│   ├── core/          # Core Python utilities
│   ├── mcp/           # MCP tool interface
│   └── agent/         # A2A agent components
├── tests/             # Unit and integration tests
├── mock_data/         # Test files (never commit real data)
├── docs/              # Documentation
└── requirements.txt   # Dependencies
```

## Testing Requirements
- Write unit tests for each parser component
- Use mock data stored in `/mock_data` directory
- Run `pytest tests/` before any commits
- Achieve minimum 80% code coverage
- Test error handling with corrupted/invalid files

## Security Guidelines
- Validate all file paths to prevent directory traversal
- Use temporary directories for extraction (auto-cleanup)
- Limit memory usage for large file processing
- Never execute extracted code or scripts
- Sanitize all user inputs

## Mock Data Requirements
Create comprehensive test files in `/mock_data`:
- mock_word.docx (Word document with text and images)
- mock_excel.xlsx (Excel with multiple sheets, formulas)
- mock_powerpoint.pptx (PowerPoint with slides, images)
- mock_powerbi.pbix (Power BI structure simulation)
- mock_tableau.twbx (Tableau workbook structure)
- mock_synapse.zip (Azure Synapse package)
- mock_archive.zip (nested folders and various file types)
- mock_source.tar.gz (source code structure)

## Implementation Notes
- **Memory efficiency**: Use streaming for large files
- **Error handling**: Plan for malformed files from the start  
- **Modularity**: Each component must be independently testable
- **Documentation**: Create usage examples for each interface
- **Performance**: Consider caching for repeated operations

## Git Workflow
- Create feature branches: `git checkout -b feature/step-X-description`
- Commit frequently with descriptive messages
- Include tests with feature implementations
- Update documentation as you go

## Pull Request Format
- Title: `[Phase X] Step Y: Brief description`
- Include:
  - What was implemented
  - Testing approach used
  - Any design decisions made
  - Next steps

## Development Phases
Work through these phases in order:
1. **Phase 1**: Core Foundation & Mock Data Setup
2. **Phase 2**: Core Python Utilities  
3. **Phase 3**: Intelligence Layer
4. **Phase 4**: MCP Tool Interface
5. **Phase 5**: A2A Agent Implementation
6. **Phase 6**: Testing & Refinement

Refer to the full development checklist for detailed step-by-step instructions.

## Notes for AI Agent
- Focus on one step at a time from the checklist
- Create working, testable code at each step
- Use mock data for all testing (no internet required)
- Ask clarifying questions if any requirements are unclear
- Prioritize functionality over optimization in early phases