# Integration Guide

This guide explains how to interact with the archive processing agent from other A2A agents or services.

## Registering an Agent
Use `AgentRegistry` to register agents along with their capabilities and optional handler function.
```python
registry = AgentRegistry()
registry.register_agent("archive-agent", {"formats": ["zip", "docx"]}, handler=my_handler)
```

## Sending Requests
Create an `AgentRequest`, convert it to a dictionary, and send it via `RequestRouter`.
```python
router = RequestRouter(registry)
request = AgentRequest(file_path="mock_data/mock_archive.zip", request_text="list files")
response = router.send_request(request.to_dict())
```

`send_request` automatically handles basic retries, rate limiting, and audit logging.

## Handling Responses
`send_request` returns a dictionary matching the `AgentResponse` structure. Check the `status` field and process the `data` accordingly.

## Troubleshooting
- Ensure the target file path exists and is accessible.
- Check the audit log via `router.get_audit_log()` for errors.
- Use `registry.check_health(name)` to verify that agents are online.

## Discovering MCP Tools

MCP tools such as `extract_archive_tool` can be registered with the
`ToolRegistry`. Agents may query the registry to discover available tools and
their capabilities.

```python
from src.mcp import extract_archive_tool, ToolRegistry
registry = ToolRegistry()
manifest = registry.load_manifest("src/mcp/manifest.json")
registry.register_tool("extract_archive", extract_archive_tool, manifest=manifest)

available = registry.discover_tools()
print(available["extract_archive"]["description"])
```

Other agents can call the tool via `registry.get_tool(name)(**params)`.
