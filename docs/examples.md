# Example Usage

The following example demonstrates how to integrate the archive processing agent into another service.

```python
from src.agent import ArchiveAgent, AgentRequest

agent = ArchiveAgent()
request = AgentRequest(file_path="mock_data/mock_archive.zip", request_text="summarize")
result = agent.process_request(request.file_path, request.request_text)
print(result["summary"])
```

For distributed setups, register the agent with an `AgentRegistry` and use a `RequestRouter` to balance requests among multiple agents.

## MCP Tool Integration

The `ToolRegistry` allows discovery and invocation of MCP tools. Register the
`extract_archive_tool` and load its manifest for other agents to discover.

```python
from src.mcp import extract_archive_tool, ToolRegistry
from pathlib import Path

registry = ToolRegistry()
manifest = registry.load_manifest(Path("src/mcp/manifest.json"))
registry.register_tool("extract_archive", extract_archive_tool, manifest=manifest)

for name, info in registry.discover_tools().items():
    print(name, info["description"])

result = registry.get_tool("extract_archive")("mock_data/mock_archive.zip")
print(result["status"])
```

Different agent types can look up the manifest to understand parameters and
call the tool directly or via their own frameworks.
