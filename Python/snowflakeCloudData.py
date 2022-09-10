import csv
from collections import defaultdict

snowflake_csv = "SnowflakeCloudData.csv"

test = {}
with open(snowflake_csv, encoding='utf-8-sig') as f:
    csv_reader = csv.DictReader(f)

    for record in csv_reader:
        # print(record.keys())
        # print(record['on_demand_price_eur'])
        for key in record:
            # print(key)
            # parts = key.split('_')
            if 'usd' in key or 'gbp' in key or 'eur' in key:

                #STORAGE COSTS
                if 'storage' in key or 'demand' in key:
                    parts = key.split('_')
                    # print(parts[0:3])
                    # if 'on_demand_price_eur' in key:
                    #     test = {'platform': {record['platform']:{record['cloudregion']:{parts[0] + '_' + parts[1] + '_' + parts[2] : {parts[3]:record['on_demand_price_eur']}}}}}
                    #     # print(test)
                    #
                    # if 'on_demand_price_usd' in key:
                    #     test = {'platform': {record['platform']:{record['cloudregion']:{parts[0] + '_' + parts[1] + '_' + parts[2] : {parts[3]:record['on_demand_price_usd']}}}}}
                    #     # print(test)
                    #
                    # if 'on_demand_price_gbp' in key:
                    #     test = {'platform': {record['platform']:{record['cloudregion']:{parts[0] + '_' + parts[1] + '_' + parts[2] : {parts[3]:record['on_demand_price_gbp']}}}}}
                    #     # print(test)
                    #
                    # if 'capacity_storage_price_eur' in key:
                    #     test = {'platform': {record['platform']:{record['cloudregion']:{parts[0] + '_' + parts[1] + '_' + parts[2] : {parts[3]:record['capacity_storage_price_eur']}}}}}
                    #     # print(test)
                    #
                    # if 'capacity_storage_price_usd' in key:
                    #     test = {'platform': {record['platform']:{record['cloudregion']:{parts[0] + '_' + parts[1] + '_' + parts[2] : {parts[3]:record['capacity_storage_price_usd']}}}}}
                    #     # print(test)
                    #
                    # if 'capacity_storage_price_gbp' in key:
                    #     test = {'platform': {record['platform']:{record['cloudregion']:{parts[0] + '_' + parts[1] + '_' + parts[2] : {parts[3]:record['on_demand_price_gbp']}}}}}
                    #     # print(test)

                #PRICES
                if 'tier' in key:
                    parts = key.split('_')
                    # print(parts[0:3])

                    if 'standard_tier_price_eur' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']:{record['cloudregion']:{'tier' : {parts[0]: {parts[3]: record['standard_tier_price_eur']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'standard_tier_price_usd' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['standard_tier_price_usd']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'standard_tier_price_gbp' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['standard_tier_price_gbp']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'enterprise_tier_price_eur' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']:{record['cloudregion']:{'tier' : {parts[0]: {parts[3]: record['enterprise_tier_price_eur']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'enterprise_tier_price_usd' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['enterprise_tier_price_usd']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'enterprise_tier_price_gbp' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['enterprise_tier_price_gbp']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'business-critical_tier_price_eur' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['business-critical_tier_price_eur']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'business-critical_tier_price_usd' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['business-critical_tier_price_usd']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    if 'business-critical_tier_price_usd' in key:
                        # tier = 'enterprise'
                        test = {'platform': {record['platform']: {record['cloudregion']: {
                            'tier': {parts[0]: {parts[3]: record['business-critical_tier_price_gbp']}}}}}}
                        # print(record['on_demand_price_eur'])
                        # print(test)

                    # print(test)
print(test)