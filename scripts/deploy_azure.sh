#!/bin/bash
# Simplified deployment script for demonstration purposes
RESOURCE_GROUP=${RESOURCE_GROUP:-archive-processing}
APP_NAME=${APP_NAME:-archive-processing-agent}

az group create --name "$RESOURCE_GROUP" --location eastus
az storage account create --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" --sku Standard_LRS
az webapp create --resource-group "$RESOURCE_GROUP" --plan B1 --name "$APP_NAME" --runtime "PYTHON|3.8"
az webapp config appsettings set --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" --settings @.env.production

echo "Deployment complete"
