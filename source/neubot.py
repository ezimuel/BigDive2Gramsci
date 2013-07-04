# BigDive2 Gramsci project 
# ------------------------
#
# Read the NeuBot CSV file, add the latitude, longitude and country name
# and store the values into MongoDB
#
# Author: Enrico Zimuel (e.zimuel@gmail.com)
# Copyright 2013 by BigDive  - http://www.bigdive.eu
#
import fileinput
import sys
import os.path
from pymongo import MongoClient  

if len(sys.argv) < 4:
    print "Usage: python neubot.py [file] [mm] [yyyy]"
    sys.exit()

if not os.path.exists(sys.argv[1]):
    print "Error: the file specified doesn't exist"
    sys.exit()

if len(sys.argv[2]) != 2:
    print "Error: The month must contains 2 digits [mm]"
    sys.exit()

if len(sys.argv[3]) != 4:
    print "Error: The year must contains 4 digits [yyyy]"
    sys.exit()
       
file_neubot = sys.argv[1]
month = sys.argv[2]
year = sys.argv[3]

client = MongoClient()
db_city = client.cities
db_neubot = client.neubot
db_country = client.countries

# Ensure index on MongoDB
db_city.city.ensure_index([('city',1), ('country',1)])
db_country.country.ensure_index('code', unique=True)

cities = {}
countries = {}

i = 0
for line in fileinput.input([file_neubot]):
    row = [x.replace('\"','').replace("\n",'') for x in line.split(', ')]
    
    # Get the geoinformation (lat,lon) for the city
    city_country = ''.join([row[14],'-',row[1].lower()])
    if not city_country in cities:
    	cities[city_country] =  db_city.city.find_one({ 'city' : row[14], 'country' : row[1].lower()})

    if (cities[city_country] == None) or (cities[city_country] == 'Error'):
        cities[city_country] = 'Error'
        continue

    # Get the full country name
    if not row[1] in countries:
        result = db_country.country.find_one({ 'code' : row[1] })
        countries[row[1]] = result['country']

    i += 1
    data = { 
        'id'        : i,
        'ip'        : row[0],
    	'download'  : float(row[4]),
    	'upload'    : float(row[10]),
    	'country'   : countries[row[1]],
    	'provider'  : row[2],
    	'city'      : row[14],
      	'lat'       : float(cities[city_country]['lat']),
       	'lon'       : float(cities[city_country]['lon']),
        'type'      : row[8],
        'month'     : month,
        'year'      : year,
        'timestamp' : row[9]
	}
    db_neubot.samples.insert(data)
    print i

print "DONE"
