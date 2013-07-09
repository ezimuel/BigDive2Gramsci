BigDive2Gramsci
===============

BigDive2 Gramsci final project of the BigDive2 course (http://www.bigdive.eu).

Project
-------

The goal of this project was to estimate the Network Neutrality (NN) based on the ADSL download data used by the NeuBot project (http://neubot.org/).
We implemented a system in Python to extract data from the samples of Neubot (CSV file) and estimate the NN based on this formula:
    
```    
NN = 1 - | ST - BT | / ST
```    

where `ST` is the Speed Test (bytes/sec) and `BT` is the BitTorrent Test (bytes/sec) retrieved from the NetBot data.
We aggregated the data by country, city and provider and putted the result on a geographic map.

We want to precise that the NN index proposed in this work is just a warning for a potential network neutrality violation. The data reported in the Neubot project are not enough to estimate a real network neutrality violation, nevertheless we think that this index can be significant if the number of Neubot clients become relevant from a statistic point of view, comparing different Internet providers.

This project has been realized for the BigDive2 course as final project in 2013 (http://www.bigdive.eu).

Requirements
------------

- Python 2.7.3 (with pymongo)
- MongoDB


How to elaborate the Network Neutrality
---------------------------------------

In order to elaborate the NN from the Neubot data you have to execute the following steps:

1) Extract the .zip files of the `/source/data` folder in the `/source` folder.

2) Execute the insert_city_mongodb.py script to populate the world city database in MongoDB:

```bash
$ python insert_city_mongodb.py
```

3) Execute the insert_country_mongodb.py to populate the country database in MongoDB:

```bash
$ python insert_country_mongodb.py
```

4) Execute the neubot.py script to insert the NeuBot data in MongoDB (adding the geoinformation about the cities):

```bash
$ python neubot.py neubot.utf8.csv 01 2013
```

The data reported here are related to January 2013 of Neubot project.

5) Execute the neutrality.py script to elaborate the Network Neutrality for each NeuBot data:

```bash
$ python neutrality.py
```    

6) Aggregate the data by country, city and provider using the aggregate_by_country.py script:

```bash
$ python aggregate_by_country.py > neutrality_country_012013.json   
```

This Json file can be used by D3.js to plot the data in a world map (this Json file is stored in the public/data folder).


How to visualize the result of the project
------------------------------------------

We implemented an interactive world map to visualize the Network Neutrality results of the collected Neubot data. We used only a subset of the Neubot dataset base on the data of January 2013. We collected the data by country, city and Internet provider. For each Internet provider we showed the Network neutrality () index using a color between red (NN=0, poor neutrality) and green (NN=1, perfect neutrality).

In order to visualize the world map you need to execute the public folder inside a web server. We suggest to use the built in web server of python without any configuration. You can go inside the public folder and execute the following command:

```bash
$ python -m SimpleHTTPServer
```
   
Now you can point your browser to the URL http://localhost:8000/Network_Neutrality.html and enjoy the interactive world map of the Neubot data (the port 8000 is the default one provided by python).


Team "Gramsci devoted"
----------------------

Giuseppe Futia (giuseppe.futia@gmail.com), Rocco Corriero (r.corriero@gmail.com), and Enrico Zimuel (e.zimuel@gmail.com).


Thanks
------

A special thanks to Simone Basso, the team leader of the Neubot project, for the assistance with the data and the general advices. 
 
