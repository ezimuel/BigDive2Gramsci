# Insert the countries in MongoDB

import fileinput
from pymongo import MongoClient

client = MongoClient()
db = client.countries
countries = {}

i = 1
for line in fileinput.input(['GeoIPCountryWhois.utf8.csv']):
    row = [x.replace("\n",'').replace("\"",'') for x in line.split(',')]
    if not row[4] in countries:
        country = { 'country' : row[5], 'code' : row[4] }
        db.country.insert(country)
        i += 1
        print i
        countries[row[4]] = row[5]

