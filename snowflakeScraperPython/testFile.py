import requests
from bs4 import BeautifulSoup
import json
import re
from collections import defaultdict
from os import path
from json import loads, dumps
from collections import defaultdict
import pandas as pd
from pandas import json_normalize

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
                                        {'id':1, 'platform': splittedSentence[0], 'cloudregion': splittedSentence[1],
                                         name[:-10]: {name.split('_')[2] + '_' + name.split('_')[3]: value.replace(',', '.')}})

            df = pd.DataFrame(dataScrapeStorageCosts)
            print(df)

        except Exception as e:
            print('An error occured while scraping the storage costs: ' + str(e))
            pass

snowflakeCalculatorScraper.scrapeStorageCosts()