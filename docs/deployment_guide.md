# Deployment Guide

This document outlines how to deploy the archive processing agent to a generic cloud environment.

1. Provision storage and a secrets manager for credentials.
2. Configure authentication so the agent can access these resources.
3. Set environment variables in your application host or container.
4. Deploy the application using your provider's CLI or CI/CD pipeline.
5. Enable monitoring and health checks using your provider's tooling.

Example CLI deployment script is provided in `scripts/deploy_azure.sh`.

## Local Deployment

Set `STORAGE_PROVIDER=local` and specify `LOCAL_STORAGE_PATH` to store files on
the local filesystem. Other settings mirror the `.env.local.example` template.
