# Archive Processing Agent

An intelligent A2A (Agent-to-Agent) system that can extract, parse, and analyze various archive formats including ZIP, TAR, Microsoft Office documents, Power BI files, Tableau workbooks, and Azure Synapse packages.

## 🎯 Project Goals

- **Intelligent Extraction**: Automatically detect and extract content from multiple archive formats
- **Contextual Processing**: Understand document structures and return relevant content based on requesting agent needs
- **Multi-Interface Support**: Provide both simple MCP tools and intelligent A2A agent capabilities
- **Offline Operation**: Work entirely with local files and mock data for testing

## 📦 Supported Formats

| Format | Extension | Capabilities |
|--------|-----------|-------------|
| **Archives** | `.zip`, `.tar`, `.tar.gz`, `.7z` | Basic extraction and file listing |
| **Office Docs** | `.docx`, `.xlsx`, `.pptx` | Text extraction, metadata, embedded content |
| **Business Intelligence** | `.pbix` (Power BI) | Data models, DAX measures, visualizations |
| **Analytics** | `.twbx` (Tableau) | Dashboards, calculated fields, data connections |
| **Cloud Platforms** | Azure Synapse packages | SQL scripts, notebooks, pipeline definitions |

## 🏗️ Architecture

```
A2A Archive Agent
├── 📚 Core Python Libraries (reusable utilities)
│   ├── archive_handler.py      # Basic ZIP/TAR extraction
│   ├── office_parser.py        # Word/Excel/PowerPoint processing  
│   ├── powerbi_parser.py       # Power BI file structure parsing
│   ├── tableau_parser.py       # Tableau workbook processing
│   ├── synapse_parser.py       # Azure Synapse package handling
│   ├── relevance_engine.py     # Content filtering and scoring
│   └── content_summarizer.py   # Intelligent summarization
├── 🔧 MCP Tool Interface (for simple operations)
│   └── mcp_tool.py             # Direct tool calls for basic extraction
└── 🤖 A2A Agent Layer (for complex processing)
    ├── archive_agent.py        # Main agent logic and conversation handling
    ├── request_interpreter.py  # Natural language request parsing
    └── response_formatter.py   # Adaptive output formatting
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- OpenAI API key (for Codex development)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd archive-processing-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests with mock data
pytest tests/
```

### Basic Usage

```python
from src.core.archive_handler import ArchiveHandler
from src.agent.archive_agent import ArchiveAgent

# Simple extraction
handler = ArchiveHandler()
contents = handler.extract_archive("path/to/file.zip")

# Intelligent processing via A2A agent
agent = ArchiveAgent()
response = agent.process_request(
    file_path="path/to/document.pbix",
    request="Extract all DAX measures and data relationships"
)
```

## 🛠️ Development

This project is designed to be developed step-by-step with OpenAI Codex. See the development workflow:

### Development Phases

1. **Phase 1**: Core Foundation & Mock Data Setup
2. **Phase 2**: Core Python Utilities
3. **Phase 3**: Intelligence Layer  
4. **Phase 4**: MCP Tool Interface
5. **Phase 5**: A2A Agent Implementation
6. **Phase 6**: Testing & Refinement

### Getting Started with Development

1. **Review the checklist**: See `DEVELOPMENT_CHECKLIST.md` for detailed step-by-step instructions
2. **Check AGENTS.md**: Contains specific guidance for AI-assisted development
3. **Start with mock data**: All development uses offline mock files
4. **Work incrementally**: Complete each step fully before proceeding

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/core/          # Core utility tests
pytest tests/integration/   # Integration tests

# Run with coverage
pytest --cov=src tests/
```

## 📁 Project Structure

```
/
├── src/
│   ├── core/              # Core Python utilities
│   │   ├── __init__.py
│   │   ├── archive_handler.py
│   │   ├── office_parser.py
│   │   ├── powerbi_parser.py
│   │   ├── tableau_parser.py
│   │   ├── synapse_parser.py
│   │   ├── relevance_engine.py
│   │   └── content_summarizer.py
│   ├── mcp/               # MCP tool interface
│   │   ├── __init__.py
│   │   └── mcp_tool.py
│   ├── agent/             # A2A agent components
│   │   ├── __init__.py
│   │   ├── archive_agent.py
│   │   ├── request_interpreter.py
│   │   └── response_formatter.py
│   └── utils/             # Shared utilities
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── core/              # Unit tests for core utilities
│   ├── integration/       # Integration tests
│   └── mock_data/         # Test files and fixtures
├── mock_data/             # Mock files for testing
│   ├── mock_word.docx
│   ├── mock_excel.xlsx
│   ├── mock_powerpoint.pptx
│   ├── mock_powerbi.pbix
│   ├── mock_tableau.twbx
│   ├── mock_synapse.zip
│   ├── mock_archive.zip
│   └── mock_source.tar.gz
├── docs/                  # Documentation
│   ├── api_reference.md
│   ├── examples.md
│   └── deployment_guide.md
├── AGENTS.md              # AI development instructions
├── DEVELOPMENT_CHECKLIST.md  # Step-by-step development guide
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔌 Usage Examples

### MCP Tool Interface (Simple Operations)

```python
# Basic file extraction
result = extract_archive("document.zip")
print(result["files"])  # List of extracted files
print(result["metadata"])  # Archive metadata
```

### A2A Agent Interface (Complex Processing)

```python
# Intelligent content extraction
agent = ArchiveAgent()

# Example 1: Extract business intelligence content
response = agent.process_request(
    file_path="quarterly_report.pbix",
    request="Get all data sources and key performance indicators"
)

# Example 2: Analyze code repository
response = agent.process_request(
    file_path="project_source.tar.gz", 
    request="Find configuration files and database connection strings"
)

# Example 3: Document analysis
response = agent.process_request(
    file_path="meeting_notes.docx",
    request="Extract action items and deadlines"
)
```

## 🧪 Mock Data

The project includes comprehensive mock data for offline development and testing:

- **Office Documents**: Word docs with text/images, Excel with formulas, PowerPoint with slides
- **BI Files**: Simulated Power BI and Tableau structures with realistic content
- **Code Archives**: Sample source code repositories with various file types
- **Complex Archives**: Nested ZIP files with mixed content types

All mock data is located in `/mock_data` and designed to test edge cases and typical usage patterns.

## 🔒 Security Features

- **Sandboxed Extraction**: All archives extracted to temporary, isolated directories
- **Path Validation**: Prevents directory traversal attacks
- **Memory Limits**: Protects against zip bombs and large file attacks  
- **Input Sanitization**: Validates all user inputs and file paths
- **No Code Execution**: Never executes extracted scripts or binaries

## 🤝 Contributing

This project is designed for AI-assisted development with OpenAI Codex. To contribute:

1. **Follow the development checklist** in `DEVELOPMENT_CHECKLIST.md`
2. **Review AGENTS.md** for AI development guidelines
3. **Work incrementally** - complete each step fully
4. **Test thoroughly** with mock data
5. **Document your changes** as you go

### Development Workflow

```bash
# Create feature branch
git checkout -b feature/phase-X-step-Y

# Make changes following the checklist
# ... development work ...

# Test your changes
pytest tests/

# Commit with descriptive message
git commit -m "[Phase X] Step Y: Brief description"

# Push and create PR
git push origin feature/phase-X-step-Y
```

## 📋 Requirements

### Core Dependencies

```txt
# Archive handling
python-docx>=0.8.11
openpyxl>=3.0.9  
python-pptx>=0.6.21
py7zr>=0.20.0

# XML/JSON processing
lxml>=4.6.3
xmltodict>=0.12.0

# Utilities
pathlib2>=2.3.6
python-magic>=0.4.24

# Testing
pytest>=6.2.4
pytest-cov>=2.12.1
```

### Optional Dependencies

```txt
# Additional archive formats
rarfile>=4.0        # For RAR support
patool>=1.12.0       # Multi-format archive tool
```

## 📄 License

[Add your license information here]

## 🆘 Support

- **Issues**: Report bugs and feature requests in the GitHub issues
- **Documentation**: See `/docs` folder for detailed API documentation
- **Examples**: Check `/docs/examples.md` for usage patterns

## 🗺️ Roadmap

- [x] **Phase 1**: Project setup and mock data creation
- [ ] **Phase 2**: Core parsing utilities  
- [ ] **Phase 3**: Intelligence and relevance filtering
- [ ] **Phase 4**: MCP tool interface
- [ ] **Phase 5**: A2A agent implementation
- [ ] **Phase 6**: Testing and optimization

---

**Built with AI assistance using OpenAI Codex** 🤖
