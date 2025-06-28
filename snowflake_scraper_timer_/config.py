"""Configuration module for Azure Functions"""
import os
from typing import Optional

def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get environment variable or raise error if not found and no default provided"""
    value = os.environ.get(var_name, default)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = get_env_variable('AZURE_STORAGE_CONNECTION_STRING')

# Azure Log Analytics Configuration
LOG_ANALYTICS_WORKSPACE_ID = get_env_variable('LOG_ANALYTICS_WORKSPACE_ID')
LOG_ANALYTICS_SHARED_KEY = get_env_variable('LOG_ANALYTICS_SHARED_KEY')

# Storage Configuration
CONTAINER_NAME = "snowflakedata"
BLOB_NAME = "SnowflakeCloudData.json"

# Log Analytics Configuration
TABLE_NAME = 'snowflake_scraper_monitor'

# Scraping Configuration
SNOWFLAKE_PRICING_URL = 'https://www.snowflake.com/pricing/'
USER_AGENT = 'Mozilla/5.0'

# Data validation thresholds
MIN_STORAGE_ITEMS = 144
MIN_PRICE_ITEMS = 102
MIN_TOTAL_ITEMS = 246