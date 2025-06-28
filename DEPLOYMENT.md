# Snowflake Calculator - Deployment Guide

## Environment Variables Setup

### Required Environment Variables

The following environment variables must be configured for the application to work properly:

#### Azure Functions Environment Variables

1. **AZURE_STORAGE_CONNECTION_STRING**
   - Description: Connection string for Azure Storage Account
   - Format: `DefaultEndpointsProtocol=https;AccountName=<account>;AccountKey=<key>;EndpointSuffix=core.windows.net`
   - Required for: Storing scraped pricing data

2. **LOG_ANALYTICS_WORKSPACE_ID**
   - Description: Azure Log Analytics Workspace ID
   - Format: GUID (e.g., `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
   - Required for: Monitoring and logging

3. **LOG_ANALYTICS_SHARED_KEY**
   - Description: Azure Log Analytics Shared Key
   - Format: Base64 encoded string
   - Required for: Authenticating to Log Analytics

4. **EXCHANGE_RATE_API_KEY**
   - Description: API key for Exchange Rate API
   - Format: Alphanumeric string
   - Required for: Currency conversion
   - Get your key at: https://app.exchangerate-api.com/sign-up

### Local Development Setup

1. Copy the example files:
   ```bash
   cp .env.example .env
   cp snowflake_scraper_timer_/local.settings.json.example snowflake_scraper_timer_/local.settings.json
   cp exchange_rate_proxy/local.settings.json.example exchange_rate_proxy/local.settings.json
   ```

2. Fill in your actual values in the `.env` and `local.settings.json` files

3. Never commit these files to version control

### Azure Deployment Setup

#### Using Azure Portal

1. Navigate to your Function App in Azure Portal
2. Go to Configuration → Application settings
3. Add the following application settings:
   - `AZURE_STORAGE_CONNECTION_STRING`
   - `LOG_ANALYTICS_WORKSPACE_ID`
   - `LOG_ANALYTICS_SHARED_KEY`
   - `EXCHANGE_RATE_API_KEY`

#### Using Azure CLI

```bash
# Set environment variables for the Function App
az functionapp config appsettings set \
  --name <function-app-name> \
  --resource-group <resource-group> \
  --settings \
    AZURE_STORAGE_CONNECTION_STRING="<connection-string>" \
    LOG_ANALYTICS_WORKSPACE_ID="<workspace-id>" \
    LOG_ANALYTICS_SHARED_KEY="<shared-key>" \
    EXCHANGE_RATE_API_KEY="<api-key>"
```

#### Using ARM Template or Bicep

Include the app settings in your infrastructure as code:

```json
{
  "appSettings": [
    {
      "name": "AZURE_STORAGE_CONNECTION_STRING",
      "value": "[parameters('storageConnectionString')]"
    },
    {
      "name": "LOG_ANALYTICS_WORKSPACE_ID",
      "value": "[parameters('logAnalyticsWorkspaceId')]"
    },
    {
      "name": "LOG_ANALYTICS_SHARED_KEY",
      "value": "[parameters('logAnalyticsSharedKey')]"
    },
    {
      "name": "EXCHANGE_RATE_API_KEY",
      "value": "[parameters('exchangeRateApiKey')]"
    }
  ]
}
```

### Frontend Configuration

The frontend uses a configuration file (`docs/js/config.js`) that can be modified for different environments:

```javascript
const CONFIG = {
    // For production, point to your Azure Functions endpoints
    SNOWFLAKE_DATA_API: "https://your-function-app.azurewebsites.net/api/snowflakeclouddatajson",
    EXCHANGE_RATE_PROXY: "https://your-function-app.azurewebsites.net/api/exchange_rate_proxy",
    
    // Set to false in production to use live data
    USE_LOCAL_DATA: false,
    
    // Set to false in production
    DEBUG_MODE: false
};
```

### Security Best Practices

1. **Use Azure Key Vault** for storing sensitive information in production
2. **Enable Managed Identity** for your Function App to access Key Vault
3. **Rotate keys regularly** - especially API keys and storage account keys
4. **Use RBAC** instead of keys where possible
5. **Enable CORS** only for your specific domain in production

### Verification

After deployment, verify that all environment variables are properly set:

1. Check Function App logs for any configuration errors
2. Test the scraper function execution
3. Verify exchange rate proxy endpoint returns data
4. Ensure frontend can fetch data from both endpoints

### Troubleshooting

If you encounter issues:

1. Check Application Insights logs
2. Verify all environment variables are set correctly
3. Ensure storage account and Log Analytics workspace exist
4. Check that API keys are valid and not expired
5. Verify CORS settings if frontend cannot access APIs