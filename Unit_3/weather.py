import datetime
import requests
import pandas as pd
from pandas.io.json import json_normalize
import sqlite3 as lite

cities = { "Chicago": '41.837551,-87.681844',
			"Cleveland": '41.478462,-81.679435',
			"Denver":'39.761850,-104.881105',
			"New York": '40.663619,-73.938589',
			"Philadelphia": '40.009376,-75.133346'
		}

api_key = "d0bf3238797f7efc5cb6a86fd1128d12"

#https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME
url = "https://api.forecast.io/forecast/"+api_key+"/"
end_date = datetime.datetime.now()

start_date = end_date - datetime.timedelta(days=30)

str_start_date = str(start_date)

#parse datetime to match api requirements
parsed_str_start_date = str_start_date[0:10]+"T"+str_start_date[11:19]

api_call_chicago = "https://api.forecast.io/forecast/"+api_key+"/"+cities["Chicago"]+","+parsed_str_start_date

r = requests.get(api_call_chicago)

#create dataframe
df = json_normalize(r.json()['daily']['data'])

#print df['temperatureMax']

con = lite.connect('weather.db')
cur = con.cursor()

the lines below create the table, but only need to run once
with con: #create a table in sqlite
	cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Chicago REAL, Cleveland REAL, Denver REAL, New York REAL, Philadelphia REAL);')

with con:
	while start_date < end_date:
		cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(start_date.strftime('%s')),))
		start_date += datetime.timedelta(days=1)

for k, v in cities.iteritems():
	query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
	while query_date < end_date:
        #query for the value
		r = requests.get(url + v + ',' + query_date.strftime('%Y-%m-%dT12:00:00'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day

con.close() # a good practice to close connection to database

# con = lite.connect('weather.db')
# cur = con.cursor()

# df = pd.read_sql_query("SELECT * FROM daily_temp", con)

# print df['day_of_reading']