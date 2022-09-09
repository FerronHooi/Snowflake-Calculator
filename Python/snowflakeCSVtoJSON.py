import csv

with open('snowflakeCloudData.csv', encoding='utf-8-sig') as csv_data:
    csv_reader = csv.DictReader(csv_data)
    # combined_col = {'platform': []}
    dict = {'platform': {'cloudplatform': {'cloudregion': {'on_demand_price': {'eur': [], 'usd': [], 'gbp': []}, 'capacity_storage_price': {'eur': [], 'usd': [], 'gbp': []}, 'tier': {'standard': {'eur':[], 'usd':[], 'gbp':[]}, 'enterprise': {'eur':[], 'usd':[], 'gbp':[]}, 'businesscritical': {'eur':[], 'usd':[], 'gbp':[]}}}}}}

    for record in csv_reader:
        print(record)
        dict['platform'].append(record['platform'])

    print(dict)