# A2A Protocol Specification

This document describes how agents communicate using standardized request and response messages.

## Message Structures

### AgentRequest
- `file_path` – path to the file or archive to analyze
- `request_text` – natural language request describing the desired operation
- `response_format` – desired response format (`markdown`, `json`, `references`, `executive`)
- `agent` – optional identifier of the requesting agent
- `metadata` – extra request metadata

### AgentResponse
- `status` – `success` or `error`
- `message` – human readable summary of the result
- `data` – parsed content or analysis results
- `metadata` – additional information such as processing times

Both structures are defined in `src/agent/protocol.py` and include helper methods for validation and conversion.

## Workflow
1. The requesting agent creates an `AgentRequest` and converts it to a dictionary.
2. The request is passed to the `RequestRouter`, which selects a suitable agent.
3. The receiving agent processes the request and returns an `AgentResponse` dictionary.
4. The router forwards the response back to the requester.

## Error Handling
Agents should return an `AgentResponse` with `status="error"` and a helpful `message` when processing fails. The router implements basic retry logic and records failures in the audit log.

## Example
```python
req = AgentRequest(file_path="mock_data/mock_archive.zip", request_text="list files")
router.send_request(req.to_dict())
```

## API Endpoints
While the archive agent is typically embedded within other systems, it exposes a minimal HTTP interface for direct integration. Implementations may vary, but a reference layout is provided below.

### `POST /process`
Submit an `AgentRequest` payload as JSON. The service returns an `AgentResponse` object.

```
POST /process
Content-Type: application/json
{
  "file_path": "mock_data/mock_archive.zip",
  "request_text": "summarize",
  "response_format": "json",
  "agent": "client-1"
}
```

### `GET /status`
Returns simple JSON status including version and health information.

```
GET /status
{
  "agent": "archive-processing-agent",
  "version": "1.0.0",
  "status": "online"
}
```

These endpoints are optional but recommended for services that need a lightweight HTTP interface in addition to direct A2A communication.
