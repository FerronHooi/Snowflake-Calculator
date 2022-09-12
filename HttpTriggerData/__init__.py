import logging

import azure.functions as func
import json
import requests
from bs4 import BeautifulSoup
import csv
import re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # create list of region and their prettier display names
    regionList = []

    # STORAGE COSTS

    # scrape the https://www.snowflake.com/pricing/ page for the storage costs

    try:
        url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(url.text, 'html.parser')

        # find the <script> that contains the storage costs
        allScripts = soup.find_all('script')

        # it is the 13th script on the website so [13] --> convert to string as is needed for the regex
        scriptStorageCost = str((allScripts[13]))

        # get only the relevant part of the script (so all the text between start and end)
        # print(scriptStorageCost)
        start = "jQuery(document).ready(function($)"
        end = "// custom select"
        result = scriptStorageCost[scriptStorageCost.find(start) + len(start):scriptStorageCost.rfind(end)]

        # split the lines by enters
        splittedResult = result.splitlines()

        # empty array
        listOfPricesStorage = []

        # empty dict
        priceDataDict = {}

        # listOfNames = ['on_demand_price_usd', 'on_demand_price_eur', 'on_demand_price_gbp',
        #                'capacity_storage_price_usd',
        #                'capacity_storage_price_eur', 'capacity_storage_price_gbp']

        listOfNames = ['on_demand_price_usd', 'on_demand_price_eur',
                       'capacity_storage_price_usd', 'capacity_storage_price_eur']

        # loop over splittedResult to get every line individually. Than remove the whitespaces before/after

        for line in splittedResult:
            if 'display_name' in line:
                # remove whitespaces before and after
                strippedLine = line.strip()

                # remove prefix 'platforms.' as that is not needed
                strippedLine = strippedLine.removeprefix('platforms.')

                # get display name
                display_name = line.split('=')[1].replace("'", '')

                # remove the whitespace from display name, capitalize first letter and remove the ;
                display_name = display_name.lstrip().title().replace(';', '')

                # get platform
                platform = strippedLine.split('.')[0]

                # get region
                region = strippedLine.split('.')[1]

                # dict for region names and pretty region names
                regionDicts = {'region': region, 'display_name': display_name}
                regionList.append(regionDicts)

            if "platforms." in line and not 'under_price' in line and not 'cta_text' in line and not 'cta_url' in line and not "{}" in line and not 'capacity_storage_price_gbp' in line and not 'on_demand_price_gbp' in line:
                # remove whitespaces before and after
                strippedLine = line.strip()

                # remove prefix 'platforms.' as that is not needed
                strippedLine = strippedLine.removeprefix('platforms.')

                # replace the currency signs
                replaceCurrencySigns = re.sub('[$, €, £]', '', strippedLine)

                # add decimals to digits
                replaceCurrencySigns = re.sub(r"([']\d\d['])", r'\1,00', replaceCurrencySigns)
                replaceCurrencySigns = replaceCurrencySigns.replace("'", "")
                replaceCurrencySigns = re.sub(r"(\d\d[,])", r'\1.', replaceCurrencySigns)
                replaceCurrencySigns = replaceCurrencySigns.replace(",.", ".")

                # reverse the string, replace dot of first occurence, reverse back

                reverseString = replaceCurrencySigns[::-1]
                replaceCharacter = reverseString.replace('.', ',', 1)
                reversedBack = replaceCharacter[::-1]

                splittedSentence = reversedBack.split(".")

                # if not '€' in strippedLine and not '$' in strippedLine:
                #     display_name = strippedLine.split('=')[1].replace("'", '')

                if len(splittedSentence) >= 3:

                    column = splittedSentence[2].split('=')

                    # remove apostrophe and ; from the value
                    value = re.sub("[' ;]", '', column[1])

                    for column[0] in splittedSentence:
                        for name in listOfNames:
                            if name in column[0]:
                                platform = splittedSentence[0]
                                region = splittedSentence[1]

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
                                        priceDataDict = {'platform': platform, 'region': reg['display_name'], 'data': {
                                            name[:-4]: {name.split('_')[3]: value.replace(',', '.')}}}
                                        listOfPricesStorage.append(priceDataDict)

                                    # print(priceDataDict)

    except Exception as e:
        print('An error occured while scraping the storage costs: ' + str(e))
        pass

    # PRICES
    try:
        url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(url.text, 'html.parser')

        # empty dict
        dataScrapePrices = {}

        # empty list
        listOfPrices = []

        # platforms
        platforms = ['microsoftazure', 'amazonwebservicesaws', 'googlecloudplatform']
        platformRegions = []

        # first get all the platforms with corresponding region name to scrape the data per platform + region
        for platform in platforms:
            resultsPlatformRegions = soup.find_all('div', {'id': lambda L: L and L.startswith(platform)})
            # print(results)

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

                        # clean up cloud platform names

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
                                dataScrapePrices = {'platform': platform, 'region': reg['display_name'], 'data': {
                                    'tier': {tier: {'eur': priceEur, 'usd': priceUsd, 'gbp': priceGbp}}}}
                                listOfPrices.append(dataScrapePrices)
                                # print(listOfPrices)

                    # print(dataScrapePrices)
    except Exception as e:
        print('An error occured while scraping the prices: ' + str(e))
        pass

    lst = listOfPricesStorage + listOfPrices

    # MERGING THE DATA BY PLATFORM, REGION

    out = {}
    for dct in lst:
        print(dct)
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

    # WRITING FILE TO AZURE BLOB STORAGE

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

        # # Upload the created file
        # with open("../Datafiles/snowflakeData.json", "rb") as data:
        #     blob_client.upload_blob(data, overwrite=True)

        blob_client.upload_blob(output, overwrite=True)

        # # Clean up
        # print("\nPress the Enter key to begin clean up")
        # input()
        #
        # print("Deleting blob container...")
        # container_client.delete_container()

        print("Done")

    except Exception as ex:
        print(ex)

    return func.HttpResponse(
        output,
        mimetype="application/json",
        status_code=200
    )

