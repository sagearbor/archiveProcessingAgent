# Azure Deployment Guide

This document outlines how to deploy the archive processing agent to Azure.

1. Create a Storage Account and Key Vault.
2. Set up a Managed Identity with access to the Key Vault and Storage Account.
3. Configure environment variables in the Azure App Service or container instance.
4. Deploy the application code using `az webapp up` or a CI/CD pipeline.
5. Enable monitoring and health checks using Azure Application Insights.

Example CLI deployment script is provided in `scripts/deploy_azure.sh`.
