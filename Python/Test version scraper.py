#TODO: CLEAN UP CODE
#TODO: DATA DIE GESCRAPED IS IN DE JUISTE FORMAT STOPPEN

# import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import csv
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
            # print(scriptStorageCost)
            start = "jQuery(document).ready(function($)"
            end = "// custom select"
            result = scriptStorageCost[scriptStorageCost.find(start)+len(start):scriptStorageCost.rfind(end)]

            #split the lines by enters
            splittedResult = result.splitlines()

            #empty array
            listOfPrices = []

            #empty dict
            priceDataDict = {}

            # listOfNames = ['on_demand_price_usd', 'on_demand_price_eur', 'on_demand_price_gbp',
            #                'capacity_storage_price_usd',
            #                'capacity_storage_price_eur', 'capacity_storage_price_gbp']

            listOfNames = ['on_demand_price_usd', 'on_demand_price_eur',
                           'capacity_storage_price_usd', 'capacity_storage_price_eur']

            #loop over splittedResult to get every line individually. Than remove the whitespaces before/after

            for line in splittedResult:
                if "platforms." in line and not 'under_price' in line and not 'cta_text' in line and not 'cta_url' in line and not 'display_name' in line and not "{}" in line and not 'capacity_storage_price_gbp' in line and not 'on_demand_price_gbp' in line:
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
                    reversedBack = snowflakeCalculatorScraper.reverseReplaceReverseback(replaceCurrencySigns, '.', ',', 1)

                    splittedSentence = reversedBack.split(".")

                    if len(splittedSentence) >= 3:

                        column = splittedSentence[2].split('=')

                        #remove apostrophe and ; from the value
                        value = re.sub("[' ;]", '', column[1])


                        for column[0] in splittedSentence:
                            for name in listOfNames:
                                if name in column[0]:
                                    # dataScrapeStorageCosts.append(
                                    #     {'platform': splittedSentence[0], 'cloudregion': splittedSentence[1],
                                    #      name[:-10] + '_' + name.split('_')[2] + '_' + name.split('_')[3]: value.replace(',', '.')})
                                    priceDataDict =  {'platform': splittedSentence[0], 'region': splittedSentence[1], 'data': { name[:-4]: {name.split('_')[3]: value.replace(',', '.')}}}
                                    listOfPrices.append(priceDataDict)

                        # print(priceDataDict)
            # print(priceDataDict)
            # print(dataScrapeStorageCosts)
            return listOfPrices

        except Exception as e:
            print('An error occured while scraping the storage costs: ' + str(e))
            pass

    @staticmethod
    def scrapePrices():
        # scrape the https://www.snowflake.com/pricing/ page for the storage costs

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
                            dataScrapePrices = {'platform':platform, 'region': region, 'data':{ 'tier':{tier: {'eur':priceEur, 'usd':priceUsd, 'gbp':priceGbp}}}}
                            listOfPrices.append(dataScrapePrices)
                            # print(listOfPrices)

            return listOfPrices

        except Exception as e:
            print('An error occured while scraping the prices: ' + str(e))
            pass


# snowflakeCalculatorScraper.scrapeStorageCosts()
# print(snowflakeCalculatorScraper.scrapePrices())

lst = snowflakeCalculatorScraper.scrapeStorageCosts() + snowflakeCalculatorScraper.scrapePrices()

for l in lst:
    print(l)

# for dict in fullList:
#     print(dict)

#-----------#
# import itertools
# import operator
#
# by_name = operator.itemgetter('region')
# result = []
#
# for region, grp in itertools.groupby(sorted(fullList, key=by_name), key=by_name):
#     data = set(itertools.chain.from_iterable(x['data'] for x in grp))
#     print(data)
#     # If order of `playing` is important use `collections.OrderedDict`
#     # playing = collections.OrderedDict.fromkeys(itertools.chain.from_iterable(x['playing'] for x in grp))
#     # print(data)
#     result.append({'region': region, 'data': data})
#
# # print(result)
#
# for res in result:
#     print(res)
#---------#
#
# from collections import OrderedDict
#
# d = OrderedDict()
# for l in fullList:
#     # print(l)
#     d.setdefault((l['platform'], l['region']), set()).add(l['data'])
#
# # [{'platform': k[0], 'region': k[1], 'data': v.pop() if len(v) == 1 else v}
# #     for k, v in d.items()]
# #
# # print(d)

# import pandas as pd
#
# # print(type(fullList))
#
# d = (pd.DataFrame(fullList)
#        .groupby(['platform', 'region'])
#        .data
#        .agg(set)
#        .reset_index()
#        .to_dict('r'))
#
# print(d)
#

# import pandas as pd
#
# d = (pd.DataFrame(lst)
#        .groupby(['platform'])
#        .agg(set)
#        .reset_index())
#
# print(d)
#
# d.to_json('test.json')
# import pandas as pd
# df_storage_costs = pd.DataFrame(snowflakeCalculatorScraper.scrapeStorageCosts())
#
# df_prices = pd.DataFrame(snowflakeCalculatorScraper.scrapePrices())
#
# #combine the two dataframes
# df_all = pd.concat([df_storage_costs, df_prices], axis=0)
#
# print(df_all)
#
#
# df = df_all.groupby('on_demand_price')
#
# print (df)
