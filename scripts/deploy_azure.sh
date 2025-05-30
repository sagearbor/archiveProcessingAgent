#!/usr/bin/env bash
# Simple deployment script for the Archive Processing Agent
set -e

RESOURCE_GROUP=${RESOURCE_GROUP:-archive-rg}
LOCATION=${LOCATION:-eastus}
STORAGE_ACCOUNT=${STORAGE_ACCOUNT:-archivestorage$RANDOM}
APP_NAME=${APP_NAME:-archive-agent-app}
KEY_VAULT=${KEY_VAULT:-archive-kv}

az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file scripts/main.bicep \
  --parameters storageAccountName=$STORAGE_ACCOUNT appName=$APP_NAME keyVaultName=$KEY_VAULT

az webapp config appsettings set \
  --resource-group "$RESOURCE_GROUP" \
  --name "$APP_NAME" \
  --settings @.env.production.example

# Optional: deploy container image
# az webapp create --resource-group "$RESOURCE_GROUP" --plan ${APP_NAME}-plan --name "$APP_NAME" --deployment-container-image-name <registry>/archive-agent:latest

