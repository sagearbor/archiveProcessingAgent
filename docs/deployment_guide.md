# Azure Deployment Guide

This document explains how to deploy the Archive Processing Agent to Azure.

## Prerequisites
- Azure subscription
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed
- Optional: [Bicep CLI](https://learn.microsoft.com/azure/azure-resource-manager/bicep/install)

## Azure Resource Setup
1. **Create a resource group**
   ```bash
   az group create --name archive-rg --location eastus
   ```
2. **Storage Account**
   ```bash
   az storage account create \
     --name <storageAccountName> \
     --resource-group archive-rg \
     --sku Standard_LRS
   ```
3. **Key Vault**
   ```bash
   az keyvault create --name <keyVaultName> --resource-group archive-rg
   ```
4. **Managed Identity** (App Service)
   ```bash
   az webapp identity assign --name <appName> --resource-group archive-rg
   ```
5. **Network Security**
   - Restrict inbound traffic to HTTPS only.
   - Use service endpoints or private links for storage and key vault access.

## Deployment Steps
### 1. Deploy Infrastructure with Bicep
Use the provided `scripts/main.bicep` template:
```bash
az deployment group create \
  --resource-group archive-rg \
  --template-file scripts/main.bicep \
  --parameters storageAccountName=<storageAccountName> \
               appName=<appName> \
               keyVaultName=<keyVaultName>
```

### 2. Build and Deploy Application
Deploy the agent to Azure App Service or Container Instances. For App Service:
```bash
az webapp up --name <appName> --resource-group archive-rg --sku B1
```
For Container Instances:
```bash
az container create \
  --name <appName> \
  --resource-group archive-rg \
  --image <registry>/archive-agent:latest \
  --dns-name-label <unique-label> \
  --environment-variables @.env.production.example
```
If you prefer Azure Functions, publish using `func azure functionapp publish`.

### 3. Configure Environment Variables
Store sensitive settings in Key Vault and reference them in App Service settings:
```bash
az webapp config appsettings set \
  --name <appName> \
  --resource-group archive-rg \
  --settings @.env.production.example
```
Use Managed Identity for the app to access Key Vault secrets securely.

### 4. CI/CD Pipeline
A GitHub Actions workflow is provided in `.github/workflows/azure-deploy.yml`. It performs a Bicep deployment and publishes the application on every push to `main`.

### 5. Health Checks and Monitoring
- Enable health check endpoint in App Service (`/health`).
- Configure alerts in Azure Monitor for failed requests and CPU usage.

## Production Environment Template
Copy `./env.production.example` and update values:
```bash
cp .env.production.example .env.production
```

## Next Steps
- Review the `scripts/deploy_azure.sh` script for automated deployment.
- Customize the Bicep template to match your environment.
