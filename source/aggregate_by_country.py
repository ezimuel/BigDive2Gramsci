# BigDive2 Gramsci project 
# ------------------------
#
# Aggregate the Network Neutrality data by country and print it as Json for D3.js
#
# Author: Enrico Zimuel (e.zimuel@gmail.com)
# Copyright 2013 by BigDive  - http://www.bigdive.eu
import sys
import math
import json
from pymongo import MongoClient  

# Calculate the Network Neutrality of a list of IPs
def neutrality(ips):
    num_samples = 0
    nn_download = 0
    nn_upload   = 0
    lat         = 0
    lon         = 0
        
    for ip in ips:
        nn_download += ip['num_samples'] * float(ip['neu_download'])
        nn_upload   += ip['num_samples'] * float(ip['neu_upload'])
        num_samples += ip['num_samples']
        lat = ip['lat']
        lon = ip['lon']
            
    nn_download /= num_samples
    nn_upload /= num_samples    

    return {
        'nn_download' : nn_download,
        'nn_upload'   : nn_upload,
        'num_client'  : ips.count(),
        'lat'         : lat,
        'lon'         : lon
    } 


client = MongoClient()
db_neubot = client.neubot

# Ensure index on MongoDB
db_neubot.neutrality.ensure_index('country')
db_neubot.neutrality.ensure_index([('country', 1), ('city', 1)])
db_neubot.neutrality.ensure_index([('country', 1), ('city', 1), ('provider', 1)])
db_neubot.neutrality.ensure_index([('country', 1), ('provider', 1)])

data = {}
countries = db_neubot.neutrality.distinct('country')
for country in countries:
    data_country = {}
    cities = db_neubot.neutrality.find({ 'country' : country}).distinct('city')
    for city in cities:
        providers = db_neubot.neutrality.find({ 'country' : country, 'city' : city }).distinct('provider')
        data_provider = {}
        for provider in providers:
            ips = db_neubot.neutrality.find({ 'country' : country, 'city' : city, 'provider' : provider })
            # Network neutrality by provider
            nn_provider = neutrality(ips)
            data_provider[provider] = {
                'nn_upload'   : nn_provider['nn_upload'],
                'nn_download' : nn_provider['nn_download'],
                'num_client'  : nn_provider['num_client']
            }

        ips = db_neubot.neutrality.find({ 'country' : country, 'city' : city })
        # Network neutrality by city
        nn_city = neutrality(ips)
        data_country[city] = {
            'nn_upload'   : nn_city['nn_upload'],
            'nn_download' : nn_city['nn_download'],
            'num_client'  : nn_city['num_client'],
            'lat'         : nn_city['lat'],
            'lon'         : nn_city['lon'],
            'providers'   : data_provider
        }

    ips = db_neubot.neutrality.find({ 'country' : country })
    # Network neutrality by country
    nn_country = neutrality(ips) 
    
    data_provider = {}
    providers = ips.distinct('provider')
    for provider in providers:
        ips = db_neubot.neutrality.find({ 'country' : country, 'provider' : provider })
        # Network neutrality by providers of country
        nn_provider = neutrality(ips)
        data_provider[provider] = {
            'nn_upload'   : nn_provider['nn_upload'],
            'nn_download' : nn_provider['nn_download'],
            'num_client'  : nn_provider['num_client']
        }
        
    data[country] = {
        'nn_upload'   : nn_country['nn_upload'],
        'nn_download' : nn_country['nn_download'],
        'num_client'  : nn_country['num_client'],
        'cities'      : data_country,
        'providers'   : data_provider
    }

data_for_d3 = {
    "type" : "cityCollection",
    "features" : data
}

json.dump(data_for_d3, sys.stdout)

