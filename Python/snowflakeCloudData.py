import csv
from collections import defaultdict

snowflake_csv = "SnowflakeCloudData.csv"

priceDataDict = {}
dictList = []

with open(snowflake_csv, encoding='utf-8-sig') as f:
    csv_reader = csv.DictReader(f)

    for record in csv_reader:
        # print(record.keys())
        # print(record['on_demand_price_eur'])
        for key in record:
            # print(key)
            # print(record['platform'])
            # parts = key.split('_')
            # if 'usd' in key or 'gbp' in key or 'eur' in key:

            currencies = ['eur', 'usd', 'gbp']
            tiers = ['standard', 'enterprise', 'business-critical']
            storages = ['on_demand', 'capacity_storage']

            #STORAGE COSTS
            if 'storage' in key or 'demand' in key:
                parts = key.split('_')
                # print(parts[0:3])
                # print(key)
                currencies = ['eur', 'usd']
                # print(parts)
                for storage in storages:
                    for currency in currencies:
                        if storage + '_price_' + currency in key:
                            # print(parts)
                            # print(key)
                            priceDataDict = {'platform': {record['platform']:{record['cloudregion']:{storage + '_price' : {currency:record[storage + '_price_' + currency]}}}}}
                            # print(priceDataDict)

            #PRICES
            if 'tier' in key:
                parts = key.split('_')
                for tier in tiers:
                    for currency in currencies:
                        if tier + '_tier_price_' + currency in key:
                            priceDataDict = {'platform': {record['platform']:{record['cloudregion']:{'tier' : {parts[0]: {parts[3]: record[tier + '_tier_price_' + currency]}}}}}}
                            # print(record['on_demand_price_eur'])
                            # print(priceDataDict)

            print(priceDataDict)

            # check if dictionary is empty
            if len(priceDataDict) != 0:
                dictList.append(priceDataDict)

# print(dictList['platform'])

# print(dictList)
