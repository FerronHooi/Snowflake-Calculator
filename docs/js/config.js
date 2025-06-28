// Configuration for the Snowflake Calculator
const CONFIG = {
    // API endpoints
    SNOWFLAKE_DATA_API: "https://snowflakedatascraper.azurewebsites.net/api/snowflakeclouddatajson",
    SNOWFLAKE_DATA_LOCAL: "SnowflakeCloudData.json",
    
    // Exchange Rate API Proxy (backend endpoint)
    EXCHANGE_RATE_PROXY: "https://snowflakedatascraper.azurewebsites.net/api/exchange_rate_proxy",
    
    // Use local data instead of API (for development)
    USE_LOCAL_DATA: true,
    
    // Enable/disable console logging
    DEBUG_MODE: false,
    
    // Fallback exchange rates (in case API fails)
    FALLBACK_RATES: {
        EUR: 0.92,
        GBP: 0.79,
        USD: 1.0
    }
};

// Export for use in other scripts
window.APP_CONFIG = CONFIG;