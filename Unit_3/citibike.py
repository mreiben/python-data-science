import requests
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas as pd

r = requests.get('http://www.citibikenyc.com/stations/json')
# print r.json().keys()

key_list = [] #unique list of keys for each station listing
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)

# print key_list

df = json_normalize(r.json()['stationBeanList'])

# df['availableBikes'].hist()
# plt.show()

# df['totalDocks'].hist()
# plt.show()

# df['availableDocks'].hist()
# plt.show()

grouped = df.groupby('statusValue').count() #returns 327 'In Service' stations & 5 'Not  In Service'

df['totalDocks'].mean() #34.6596385542
df['totalDocks'].median() #33.0

df_in_service = df[df.statusValue == 'In Service']

df_in_service['totalDocks'].mean() #34.9021406728
df_in_service['totalDocks'].median() #34.0

import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

#the lines below create the table, but only need to run once
# with con: #create a table in sqlite for the static values
#     cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

# #a prepared SQL statement we're going to execute over and over again
# sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

# #for loop to populate values in the database
# with con:
#     for station in r.json()['stationBeanList']:
#         #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
#         cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

#the lines below create the table, but only need to run once
#create the table for the dynamic values
#in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)
# with con:
#     cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

# a package with datetime objects
import time

# a package for parsing a string into a Python datetime object
from dateutil.parser import parse 

import collections

for i in xrange(60):
    #download the data again
    r = requests.get('http://www.citibikenyc.com/stations/json')

    #a prepared SQL statement we're going to execute over and over again
    sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

    #for loop to populate values in the database
    with con:
        for station in r.json()['stationBeanList']:
            #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
            cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

    #take the string and parse it into a Python datetime object
    exec_time = parse(r.json()['executionTime'])

    #create an entry for the execution time by inserting it into the db
    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

    id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

    #loop through the stations in the station list, populating the number of available bikes under the station id
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    #iterate through the defaultdict to update the values in the database
    with con:
        for k, v in id_bikes.iteritems():
            cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")

    time.sleep(60)