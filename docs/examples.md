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
