# Troubleshooting and Debugging

This document lists common issues when using the archive processing agent and how to resolve them.

## Common Problems
- **Unauthorized**: ensure a valid token is passed to the agent or disable authentication in tests.
- **File Not Found**: verify the `file_path` parameter and check the working directory.
- **Rate Limit Exceeded**: the router only allows a certain number of requests per minute. Increase the limit or slow down request rate.
- **Agent Offline**: check the agent status with `registry.check_health()` and ensure the process is running.
- **Parsing Errors**: if a file cannot be processed, inspect the `message` field in the `AgentResponse` for details.

## Debugging Tips
- Enable debug logging by setting `LOG_LEVEL=DEBUG` in the environment.
- Review the audit log via `router.get_audit_log()` to trace recent requests and failures.
- Use `router.get_traces()` to examine timing information for each request.
