import requests
from bs4 import BeautifulSoup
import json
import re

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
                    reversedBack = snowflakeCalculatorScraper.reverseReplaceReverseback(replaceCurrencySigns, '.', '.', 1)

                    splittedSentence = reversedBack.split('.')
                    if len(splittedSentence) >= 3:

                        column = splittedSentence[2].split('=')

                        #remove apostrophe and ; from the value
                        value = re.sub("[' ;]", '', column[1])
                        data = {'platform': splittedSentence[0], 'cloudregion': splittedSentence[1], column[0]:value}

                        print(data)
        except:
            print('An error occured while scraping the storage costs')
            pass

    @staticmethod
    def scrapePrices():
        # scrape the https://www.snowflake.com/pricing/ page for the storage costs

        try:
            url = requests.get('https://www.snowflake.com/pricing/', headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(url.text, 'html.parser')

            #empty dictionary
            data = {'platform': [], 'cloudregion': [], 'price': []}

            #get the tier
            platforms = ['microsoftazure', 'amazonewebserviceaws', 'googlecloudplatform']

            for platform in platforms:
                results = soup.find_all('div', {'id': lambda L: L and L.startswith(platform)})

                for result in results:
                    if result != None:
                        platformAndRegion = result.attrs['id']
                        platformAndRegion = platformAndRegion.split('-')
                        platform = platformAndRegion[0]
                        region = platformAndRegion[1]
                        # print({'platform': platform, 'cloudregion': region})

                        tiers = ['standard', 'enterprise', 'business-critical']

                        for tier in tiers:
                            resultsTiers = soup.find_all('div', {'id': lambda L: L and L.startswith(tier)})
                            for result in resultsTiers:
                                price = result.find(attrs={"data-price-eur" : True})
                                if price != None:
                                    priceUsd = price['data-price-usd']
                                    priceEur = price['data-price-eur']
                                    priceGbp = price['data-price-gbp']

                                    # print(priceUsd)
                                    # print(priceEur)
                                    # print(priceGbp)

                                    print({'platform': platform, 'cloudregion': region, 'tier': tier, 'price': {'price_eur': priceEur, 'price_usd': priceUsd, 'price_gbp': priceGbp}})
        except:
            print('An error occured while scraping the prices')
            pass


# print(snowflakeCalculatorScraper.scrapeStorageCosts())
print(snowflakeCalculatorScraper.scrapePrices())


