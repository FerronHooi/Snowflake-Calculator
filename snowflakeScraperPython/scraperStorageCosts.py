import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
# from AzureBlob import write_to_blob

class snowflakeCalculatorScraper:
    @staticmethod
    def reverseReplaceReverseback(string, characterToReplace, characterToReplaceWith, count):
        reverseString = string[::-1]
        replaceCharachter = reverseString.replace(characterToReplace, characterToReplaceWith, count)
        reverseStringBack = replaceCharachter[::-1]
        return reverseStringBack

    @staticmethod
    def scrapeStorageCosts():
        try:
            # scrape the https://www.snowflake.com/pricing/ page for the storage costs

            url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})
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
            dataScrapeStorageCosts = []

            listOfNames = ['on_demand_price_usd', 'on_demand_price_eur', 'on_demand_price_gbp',
                           'capacity_storage_price_usd',
                           'capacity_storage_price_eur', 'capacity_storage_price_gbp']

            #loop to over splittedResult to get every line individually. Than remove the whitespaces before/after

            for line in splittedResult:
                if "platforms." in line and not 'under_price' in line and not 'cta_text' in line and not 'cta_url' in line:
                    #remove whitespaces before and after
                    strippedLine = line.strip()

                    #remove prefix 'platforms.' as that is not needed
                    strippedLine = strippedLine.removeprefix('platforms.')

                    #replace the currency signs
                    replaceCurrencySigns = re.sub('[$, €, £]', '', strippedLine)

                    #reverse the string, replace dot of first occurence, reverse back
                    reversedBack = snowflakeCalculatorScraper.reverseReplaceReverseback(replaceCurrencySigns, '.', ',', 1)

                    splittedSentence = reversedBack.split('.')
                    if len(splittedSentence) >= 3:

                        column = splittedSentence[2].split('=')

                        #remove apostrophe and ; from the value
                        value = re.sub("[' ;]", '', column[1])


                        for column[0] in splittedSentence:
                            for name in listOfNames:
                                if name in column[0]:
                                    dataScrapeStorageCosts.append(
                                        {'platform': splittedSentence[0], 'cloudregion': splittedSentence[1],
                                         name[:-10]: {name.split('_')[2] + '_' + name.split('_')[3]: value.replace(',', '.')}})

            print (dataScrapeStorageCosts)
            return dataScrapeStorageCosts

        except Exception as e:
            print('An error occured while scraping the storage costs: ' + str(e))
            pass

    @staticmethod
    def scrapePrices():
        # scrape the https://www.snowflake.com/pricing/ page for the storage costs

        try:
            url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(url.text, 'html.parser')

            #empty array
            dataScrapePrices = []

            #platforms
            platforms = ['microsoftazure', 'amazonwebservicesaws', 'googlecloudplatform']
            platformRegions = []

            #first get all the platforms with corresponding region name to scrape the data per platform + region
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
                            dataScrapePrices.append({'platform':platform, 'cloudregion':region, 'tier': { tier: {'price_eur': priceEur, 'price_usd': priceUsd, 'price_gbp': priceGbp}}})

            return dataScrapePrices

        except Exception as e:
            print('An error occured while scraping the prices: ' + str(e))
            pass

    @staticmethod
    #function to write file to JSON
    def writeToJson():
        try:
            dataStorageCosts = snowflakeCalculatorScraper.scrapeStorageCosts()
            dataScrapePrices = snowflakeCalculatorScraper.scrapePrices()

            allData = dataStorageCosts + dataScrapePrices

            allData = json.dumps(allData, indent=4, sort_keys=True)
            # print(allData)
            with open('SnowflakeCloudData.json', 'w') as outfile:
                outfile.write(allData)

        except Exception as e:
            print('An error occured while writing the file to JSON: ' + str(e))
            pass


snowflakeCalculatorScraper.writeToJson()

# df1 = pd.DataFrame(snowflakeCalculatorScraper.scrapeStorageCosts())
# df2 = pd.DataFrame(snowflakeCalculatorScraper.scrapePrices())
# df1 = pd.merge(df1, df1, on=['cloudregion'], how='left')
# df1.to_json('SnowflakeCloudDataStorage.json', orient='records')
#
# print(df1.values)

df = pd.DataFrame({'a': [1, 2, 3, 4],
                   'b': [6, 7, 8, 9]})

print(df)

#write dateframe to json
# df.to_json('SnowflakeCloudData.json', orient='records')

# ENABLE BELOW TO WRITE FILE TO BLOB
# write_to_blob()
