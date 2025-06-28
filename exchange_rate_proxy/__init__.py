import logging
import azure.functions as func
import requests
import json
import os
from datetime import datetime, timedelta

# Cache for exchange rates
_cache = {
    'data': None,
    'timestamp': None
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Exchange rate proxy function processed a request.')

    # Get API key from environment variable
    api_key = os.environ.get('EXCHANGE_RATE_API_KEY')
    if not api_key:
        return func.HttpResponse(
            json.dumps({"error": "Exchange rate API not configured"}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

    # Check if we have cached data that's less than 1 hour old
    now = datetime.now()
    if _cache['data'] and _cache['timestamp'] and (now - _cache['timestamp'] < timedelta(hours=1)):
        logging.info('Returning cached exchange rates')
        return func.HttpResponse(
            json.dumps(_cache['data']),
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )

    try:
        # Fetch fresh exchange rates
        response = requests.get(
            f'https://v6.exchangerate-api.com/v6/{api_key}/latest/usd',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract only the rates we need to minimize response size
            filtered_data = {
                "result": data.get("result"),
                "base_code": data.get("base_code"),
                "conversion_rates": {
                    "EUR": data["conversion_rates"].get("EUR"),
                    "GBP": data["conversion_rates"].get("GBP"),
                    "USD": 1.0
                },
                "time_last_update_utc": data.get("time_last_update_utc")
            }
            
            # Update cache
            _cache['data'] = filtered_data
            _cache['timestamp'] = now
            
            return func.HttpResponse(
                json.dumps(filtered_data),
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Cache-Control": "public, max-age=3600"
                }
            )
        else:
            logging.error(f'Exchange rate API returned status code: {response.status_code}')
            return func.HttpResponse(
                json.dumps({"error": "Failed to fetch exchange rates"}),
                status_code=response.status_code,
                headers={"Content-Type": "application/json"}
            )
            
    except requests.exceptions.Timeout:
        logging.error('Exchange rate API request timed out')
        return func.HttpResponse(
            json.dumps({"error": "Request timed out"}),
            status_code=504,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        logging.error(f'Error fetching exchange rates: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )