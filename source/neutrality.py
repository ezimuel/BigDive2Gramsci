# BigDive2 Gramsci project 
# ------------------------
# Estimate the download/upload network neutrality for each IP address
#
# Author: Enrico Zimuel (e.zimuel@gmail.com)
# 
# Copyright 2013 by BigDive  - http://www.bigdive.eu
import math
from pymongo import MongoClient  

client = MongoClient()
db_neubot = client.neubot

# Ensure index on MongoDB
db_neubot.neutrality.ensure_index('ip', unique=True)
db_neubot.samples.ensure_index([('ip',1), ('type',1)])

num_ip = 0
ips = db_neubot.samples.distinct('ip')
for ip in ips:

    ip_speedtest = db_neubot.samples.find({ 'ip': ip, 'type' : 'speedtest' })
    ip_bittorrent = db_neubot.samples.find({ 'ip' : ip, 'type' : 'bittorrent' })

    if (ip_speedtest.count() == 0) or (ip_bittorrent.count() == 0):
        continue
    
    num = min(ip_speedtest.count(), ip_bittorrent.count())
    st_download  = 0
    bt_download  = 0
    st_upload    = 0
    bt_upload    = 0
    
    i = num - 1
    while i >= 0:
        st_download += ip_speedtest[i]['download']
        bt_download += ip_bittorrent[i]['download']
        st_upload   += ip_speedtest[i]['upload']
        bt_upload   += ip_bittorrent[i]['upload']
        i -= 1

    st_download /= num
    bt_download /= num
    st_upload   /= num
    bt_upload   /= num

    #Neutrality
    nn_upload   = 1 - math.fabs( st_upload - bt_upload ) / st_upload
    nn_download = 1 - math.fabs( st_download - bt_download ) / st_download
   
    ips = ip_speedtest[0]
     
    db_neubot.neutrality.save ({
        'ip'           : ips['ip'],
        'city'         : ips['city'],
        'country'      : ips['country'],
        'provider'     : ips['provider'],
        'neu_download' : nn_download,
        'neu_upload'   : nn_upload,
        'lon'          : ips['lon'],
        'lat'          : ips['lat'],
        'month'        : ips['month'],
        'year'         : ips['year'],
        'num_samples'  : num
    })
    num_ip += 1
    print num_ip

print "DONE"

