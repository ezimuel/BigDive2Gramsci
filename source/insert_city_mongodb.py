# Insert the world cities in MongoDB

import fileinput
from pymongo import MongoClient

client = MongoClient()
db = client.cities

i = 1
for line in fileinput.input(['worldcitiespop.utf8.txt']):
    row = line.split(',')
    try:
        city = { 'country' : row[0], 'city' : row[2], 'lat' : row[5], 'lon' : row[6] }
	db.city.insert(city)
        i += 1
        print i
    except:
 	continue

