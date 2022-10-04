import datetime
import logging
import azure.functions as func
import json
import requests
from bs4 import BeautifulSoup
import csv
import re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import logging
import datetime
import hashlib
import hmac
import base64
import urllib3



def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # create list of region and their prettier display names
regionList = []

#STORAGE COSTS

# scrape the https://www.snowflake.com/pricing/ page for the storage costs

try:
    url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})

    # if str(url) == "<Response [404]>":
    #     print("404 error")

    soup = BeautifulSoup(url.text, 'html.parser')

    #find the <script> that contains the storage costs
    allScripts = soup.find_all('script')

    #it is the 13th script on the website so [13] --> convert to string as is needed for the regex
    scriptStorageCost = str((allScripts[13]))

    #get only the relevant part of the script (so all the text between start and end)
    start = "jQuery(document).ready(function($)"
    end = "// custom select"
    result = scriptStorageCost[scriptStorageCost.find(start)+len(start):scriptStorageCost.rfind(end)]

    #split the lines by enters
    splittedResult = result.splitlines()

    #empty array
    listOfPricesStorage = []

    #empty dict
    priceDataDict = {}


    listOfNames = ['on_demand_price_usd', 'on_demand_price_eur',
                   'capacity_storage_price_usd', 'capacity_storage_price_eur']

    #loop over splittedResult to get every line individually. Than remove the whitespaces before/after
    for line in splittedResult:
        if 'display_name' in line:
            #remove whitespaces before and after
            strippedLine = line.strip()

            #remove prefix 'platforms.' as that is not needed
            strippedLine = strippedLine.removeprefix('platforms.')

            #get display name
            display_name = line.split('=')[1].replace("'", '')

            #remove the whitespace from display name, capitalize first letter and remove the ;
            display_name = display_name.lstrip().title().replace(';', '')

            #get platform
            platform = strippedLine.split('.')[0]

            #get region
            region = strippedLine.split('.')[1]


            #dict for region names and pretty region names
            regionDicts = {'region':region, 'display_name':display_name}
            regionList.append(regionDicts)

        if "platforms." in line and not 'under_price' in line and not 'cta_text' in line and not 'cta_url' in line and not "{}" in line and not 'capacity_storage_price_gbp' in line and not 'on_demand_price_gbp' in line:
            #remove whitespaces before and after
            strippedLine = line.strip()

            #remove prefix 'platforms.' as that is not needed
            strippedLine = strippedLine.removeprefix('platforms.')

            #replace the currency signs
            replaceCurrencySigns = re.sub('[$, €, £]', '', strippedLine)

            #add decimals to digits
            replaceCurrencySigns = re.sub(r"([']\d\d['])", r'\1,00', replaceCurrencySigns)
            replaceCurrencySigns = replaceCurrencySigns.replace("'", "")
            replaceCurrencySigns = re.sub(r"(\d\d[,])", r'\1.', replaceCurrencySigns)
            replaceCurrencySigns = replaceCurrencySigns.replace(",.", ".")

            #reverse the string, replace dot of first occurence, reverse back

            reverseString = replaceCurrencySigns[::-1]
            replaceCharacter = reverseString.replace('.', ',', 1)
            reversedBack = replaceCharacter[::-1]

            splittedSentence = reversedBack.split(".")

            if len(splittedSentence) >= 3:

                column = splittedSentence[2].split('=')

                #remove apostrophe and ; from the value
                value = re.sub("[' ;]", '', column[1])


                for column[0] in splittedSentence:
                    for name in listOfNames:
                        if name in column[0]:
                            platform = splittedSentence[0]
                            region = splittedSentence[1]

                            #cleans up the platform name
                            if platform == 'amazonwebservicesaws':
                                platform = 'Amazon Web Services (AWS)'
                            elif platform == 'googlecloudplatform':
                                 platform = 'Google Cloud Platform'
                            elif platform == 'microsoftazure':
                                platform = 'Microsoft Azure'
                            else:
                                platform = platform

                            for reg in regionList:
                                if reg['region'] == region:
                                    priceDataDict =  {'platform': platform, 'region': reg['display_name'], 'data': { name[:-4]: {name.split('_')[3]: value.replace(',', '.')}}}
                                    listOfPricesStorage.append(priceDataDict)

except Exception as e:
    print('An error occured while scraping the storage costs: ' + str(e))
    pass


# PRICES
try:
    url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(url.text, 'html.parser')

    #empty dict
    dataScrapePrices = {}

    #empty list
    listOfPrices = []

    #platforms
    platforms = ['microsoftazure', 'amazonwebservicesaws', 'googlecloudplatform']
    platformRegions = []

    #first get all the platforms with corresponding region name to scrape the data per platform + region
    for platform in platforms:
        resultsPlatformRegions = soup.find_all('div', {'id': lambda L: L and L.startswith(platform)})

        for result in resultsPlatformRegions:
            if result != None:

                platformAndRegions = result.attrs['id']
                platformRegions.append(platformAndRegions)

    for platReg in platformRegions:
        results = soup.find_all('div', {'id': platReg})

        platformAndRegions = platReg.split('-')
        platform = platformAndRegions[0]
        region = platformAndRegions[1]

        for result in results:
            tiers = ['standard', 'enterprise', 'business-critical']
            for tier in tiers:
                standardTierCosts = result.find('div', {'id': tier})
                price = standardTierCosts.find(attrs={"data-price-eur": True})
                if price != None:
                    priceUsd = re.sub('[$, €, £]', '', price['data-price-usd'])
                    priceEur = re.sub('[$, €, £]', '', price['data-price-eur'])
                    priceGbp = re.sub('[$, €, £]', '', price['data-price-gbp'])

                    #clean up cloud platform names

                    if platform == 'amazonwebservicesaws':
                        platform = 'Amazon Web Services (AWS)'
                    elif platform == 'googlecloudplatform':
                        platform = 'Google Cloud Platform'
                    elif platform == 'microsoftazure':
                        platform = 'Microsoft Azure'
                    else:
                        platform = platform

                    for reg in regionList:
                        if reg['region'] == region:
                            dataScrapePrices = {'platform':platform, 'region': reg['display_name'], 'data':{'tier':{tier: {'eur':priceEur, 'usd':priceUsd, 'gbp':priceGbp}}}}
                            listOfPrices.append(dataScrapePrices)

except Exception as e:
    print('An error occured while scraping the prices: ' + str(e))
    pass

lst = listOfPricesStorage + listOfPrices

# MERGING THE DATA BY PLATFORM, REGION
out = {}
for dct in lst:
    if "tier" in dct["data"]:
        out.setdefault(dct["platform"], {}).setdefault(
            dct["region"], {}
        ).setdefault("tier", {}).setdefault(
            (n := list(dct["data"]["tier"])[0]), {}
        ).update(
            dct["data"]["tier"][n]
        )

    else:
        out.setdefault(dct["platform"], {}).setdefault(
            dct["region"], {}
        ).setdefault((n := list(dct["data"])[0]), {}).update(dct["data"][n])

output = json.dumps(out, indent=4)

# BELOW FUNCTIONS ARE NEEDED FOR LOG ANALYTICS
def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    """Returns authorization header which will be used when sending data into Azure Log Analytics"""

    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, 'UTF-8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode(
        'utf-8')
    authorization = "SharedKey {}:{}".format(customer_id, encoded_hash)
    return authorization


def post_data(customer_id, shared_key, body, log_type):
    """Sends payload to Azure Log Analytics Workspace

    Keyword arguments:
    customer_id -- Workspace ID obtained from Advanced Settings
    shared_key -- Authorization header, created using build_signature
    body -- payload to send to Azure Log Analytics
    log_type -- Azure Log Analytics table name
    """

    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)

    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri, data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        logging.info('Accepted payload:' + body)
    else:
        logging.error("Unable to Write: " + format(response.status_code))

azure_log_customer_id = '471ef5ef-b0e4-42f2-80ae-aaba17c0405b'
azure_log_shared_key =  'QDc9toRWv2HrjLNhYcrACGs6yw8IGFCo0cKr6lwjRneC0c4B8CnaciszbMeKfyixsUQplAKi1/E42CCtZ8zRIA=='

table_name = 'snowflake_scraper_monitor'

# THIS PART IS ERROR HANDLING. 144 IS THE ORIGNAL NUMBER OF ITEMS IN LISTOFPRICESSTORAGE, 102 FOR LISTOFPRICES. 206 IN TOTAL
# IF THE NUMBER OF ITEMS IS LOWER OR HIGHER THAN 206, DATA IS NOT UPDATED.
# PLEASE CHECK THE OUTCOME OF THE SCRAPE AND UPDATE THE NUMBER OF TOTAL ITEMS IN THE LIST, IF IT STILL WORKING ACCORDINGLY

if len(listOfPricesStorage) >= 144:
    print('Storage costs successfully scraped')
else:
    print(f'Storage costs might NOT successfully scraped, there might be some changes. The original counts was 144, now it is: {len(listOfPricesStorage)}')

if len(listOfPrices) >= 102:
    print('Prices successfully scraped')
else:
    print(f'Prices might NOT successfully scraped, there might be some changes. The original counts was 102, now it is: {len(listOfPrices)}')

# DATA IS ONLY UPDATED IN THE BLOB STORAGE WHEN THE NUMBER OF ITEMS IN THE LIST IS 206
if len(lst) >= 246:
    lengthList = len(lst)
    status = (f'Data succesfully scraped, there are {lengthList} items in the list')
    try:
        connect_str = "DefaultEndpointsProtocol=https;AccountName=snowflakecalculatordata;AccountKey=2QlRyOr9e9UQagpZGxzKam3lp4vpU+pokDKDdqt63EgbGP5dCrWQhVKaqGCZJRHd8whE4nBl1meV+ASt5nncdA==;EndpointSuffix=core.windows.net"
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        container_name = "snowflakedata"
        blob_name = "SnowflakeCloudData.json"

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(

            container=container_name, blob=blob_name)

        print("\nUploading to Azure Storage as blob:\n\t" + blob_client.blob_name)

        blob_client.upload_blob(output, overwrite=True)

        print("Done")

    except Exception as ex:
     print(ex)

    data = {
        "status": "ok",
        "full_status": status,
        "number_of_records_listOfPricesStorage": len(listOfPricesStorage),
        "number_of_records_listOfPrices": len(listOfPrices),
        "number_of_records_total": len(lst),
        "blob_upload": "yes"
    }
    data_json = json.dumps(data)

    try:
        post_data(azure_log_customer_id, azure_log_shared_key, data_json, table_name)
    except Exception as error:
        logging.error("Unable to send data to Azure Log")
        logging.error(error)
else:
    status = (f'Data might NOT successfully scraped, there might be some changes. The original count was 246, now it is: {len(lst)}')
    data = {
        "status": "error",
        "full_status": status,
        "number_of_records_listOfPricesStorage": len(listOfPricesStorage),
        "number_of_records_listOfPrices": len(listOfPrices),
        "number_of_records_total": len(lst),
        "blob_upload": "no"
    }
    data_json = json.dumps(data)

    try:
        post_data(azure_log_customer_id, azure_log_shared_key, data_json, table_name)
    except Exception as error:
        logging.error("Unable to send data to Azure Log")
        logging.error(error)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
