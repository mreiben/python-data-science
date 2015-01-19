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
#rename id column to avoid SQL error
df.rename(columns={'id': 'station_id'}, inplace=True)

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
#     cur.execute('CREATE TABLE citibike_reference (station_id INT, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

# #a prepared SQL statement we're going to execute over and over again
# sql = "INSERT INTO citibike_reference (station_id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

# #for loop to populate values in the database
# with con:
#     for station in r.json()['stationBeanList']:
#         #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
#         cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

# #extract the column from the DataFrame and put them into a list
# station_ids = df['station_id'].tolist() 

# #add the '_' to the station name and also add the data type for SQLite
# station_ids = ['_' + str(x) + ' INT' for x in station_ids]

# #the lines below create the table, but only need to run once
# #create the table for the dynamic values
# #in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)
# with con:
#     cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

# a package with datetime objects
import time
import datetime

# a package for parsing a string into a Python datetime object
from dateutil.parser import parse 

import collections

# for i in xrange(60):
#     #download the data again
#     r = requests.get('http://www.citibikenyc.com/stations/json')
#     #for loop to populate values in the database

#     #a prepared SQL statement we're going to execute over and over again
#     sql = "INSERT INTO citibike_reference (station_id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#     with con:
#         for station in r.json()['stationBeanList']:
#             #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
#             cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#     #take the string and parse it into a Python datetime object
#     exec_time = parse(r.json()['executionTime'])

#     #create an entry for the execution time by inserting it into the db
#     with con:
#         cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

#     id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

#     #loop through the stations in the station list, populating the number of available bikes under the station id
#     for station in r.json()['stationBeanList']:
#         id_bikes[station['id']] = station['availableBikes']

#     #iterate through the defaultdict to update the values in the database
#     with con:
#         for k, v in id_bikes.iteritems():
#             cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")

#     time.sleep(60)

con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time", con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist() #sets all values in the column to a list
    station_id = col[1:] #trims the "_"from the column name
    station_change = 0 #defines variable to track total change between each timestamp
    for k,v in enumerate(station_vals): #returns the index (k) as well as the item (v)
        if k < len(station_vals) - 1: #repeat until 2nd to last value in the list
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #saves the total change to the hour_change dictionary for each station id

#find the station with the highest number of changes over the hour tracked in the db

def keyWithMaxVal(d):
    # create a list of the dict's keys and values;
    v = list(d.values())
    k = list(d.keys())

    #return the station (k) with the max value (v)
    return k[v.index(max(v))]

#define a variable to store the station with the highest volumne of change
max_station = keyWithMaxVal(hour_change)

#query sqlite for reference information
cur.execute("SELECT station_id, stationname, latitude, longitude FROM citibike_reference WHERE station_id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[max_station]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

plt.bar(hour_change.keys(), hour_change.values())
plt.show()