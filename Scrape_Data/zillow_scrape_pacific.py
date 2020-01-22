from __future__ import print_function, division
import requests
from lxml import html
from lxml import etree
import argparse
import unicodecsv as csv
import json
import uuid
import time

requests.__path__
headers= {
                            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'accept-encoding':'gzip, deflate, sdch, br',
                            'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                            'cache-control':'max-age=0',
                            'upgrade-insecure-requests':'1',
                            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                }

def detail_page(suffix):
    final = []
    url = 'https://www.zillow.com' + suffix
    time.sleep(1)
    response = requests.get(url, headers=headers)
    detail = html.fromstring(response.text)
    parking = detail.xpath("//*[contains(@class, 'zsg-icon-parking')]/../..//div[@class='hdp-fact-ataglance-value' or @class='fact-value' or @class='a']//text()")
    year = detail.xpath("//*[contains(@class, 'zsg-icon-calendar')]/../..//div[@class='hdp-fact-ataglance-value' or @class='fact-value' or @class='a']//text()")
    building_type = detail.xpath("//*[contains(@class, 'zsg-icon-buildings')]/../..//div[@class='hdp-fact-ataglance-value' or @class='fact-value' or @class='a']//text()")
    last_sold_on = detail.xpath("//*[contains(@class, 'zsg-lg-1-3 zsg-md-1-1')]/../..//div[contains(@class , 'zsg-fineprint date-sold')]//text()")
    # print(parking)
    # print(year)
    # print(building_type)
    # print(last_sold_on)
    return dict(parking=parking, building_type = building_type, year_built=year, last_sold_on=last_sold_on)

def zillow_data(page):
    properties_list = []
    for i in range(1, page + 1):
        url = 'https://www.zillow.com/homes/recently_sold/Daly-City-CA/15464672_zpid/31163_rid/globalrelevanceex_sort/37.71859,-122.391644,37.638839,-122.514039_rect/12_zm/' + str(i) + '_p/'
        # url = 'https://www.zillow.com/homes/recently_sold/San-Mateo-CA/13699_rid/37.598116,-122.242041,37.518372,-122.368727_rect/12_zm/' + str(i) + '_p/'
        time.sleep(1)
        print(url)

        response = requests.get(url, headers=headers)

        parser = html.fromstring(response.text)
        search_results = parser.xpath("//div[@id='search-results']//article")
        for properties in search_results:
            raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
            raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
            raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
            raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
            raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
            raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
            raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
            raw_title = properties.xpath(".//h4//text()")
            details_url = properties.xpath(".//a/@href")
            print(details_url[0])
            details = detail_page(details_url[0])

            address = ' '.join(' '.join(raw_address).split()) if raw_address else None
            city = ''.join(raw_city).strip() if raw_city else None
            state = ''.join(raw_state).strip() if raw_state else None
            postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
            price = ''.join(raw_price).strip() if raw_price else None
            info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
            broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
            title = ''.join(raw_title) if raw_title else None


            properties = {
                            'address':address,
                            'city':city,
                            'state':state,
                            'postal_code':postal_code,
                            'price':price,
                            'facts and features':info,
                            'real estate provider':broker,
                            'title':title,
                            'parking':details['parking'],
                            'year_built':details['year_built'],
                            'building_type':details['building_type'],
                            'last_sold_on':details['last_sold_on']
            }
            properties_list.append(properties)

    return properties_list

with open('zillow_data_daly_city.json', 'w') as fp:
    json.dump(zillow_data(20), fp)

# import json
# with open('zillow_data.json', 'r') as fp:
#     data = json.load(fp)

# from collections import defaultdict
# new_data = {}
# new_data = defaultdict(lambda:[],new_data)
# for i in data:
#     new_data['address'].append(i['address'])
#     new_data['city'].append(i['city'])
#     new_data['state'].append(i['state'])
#     new_data['postal_code'].append(i['postal_code'])
#     new_data['price'].append(i['price'])
#     new_data['facts and features'].append(i['facts and features'])
#     new_data['real estate provider'].append(i['real estate provider'])
#     new_data['title'].append(i['title'])

# import pandas as pd

# df = pd.DataFrame.from_dict(new_data)


# print(df)
