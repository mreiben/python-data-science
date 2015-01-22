import datetime
import requests
import pandas as pd
from pandas.io.json import json_normalize
import sqlite3 as lite

cities = { "Chicago": '41.837551,-87.681844',
			"Cleveland": '41.478462,-81.679435',
			"Denver":'39.761850,-104.881105',
			"NewYork": '40.663619,-73.938589',
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

api_call_chicago = url + cities["Chicago"]+","+parsed_str_start_date

# r = requests.get(api_call_chicago)

# #create dataframe
# df = r.json()['daily']['data'][0]['temperatureMax']

#print df['temperatureMax']

con = lite.connect('weather.db')
cur = con.cursor()

#the lines below create the table, but only need to run once
with con: #create a table in sqlite
	cur.execute('DROP TABLE IF EXISTS daily_temp')
	cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Chicago REAL, Cleveland REAL, Denver REAL, NewYork REAL, Philadelphia REAL);')

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
		#increment query_date to the next day for the next operation of the loop
		query_date += datetime.timedelta(days=1)

con.close() # a good practice to close connection to database

con = lite.connect('weather.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM daily_temp", con)

print df[0:3]

for k, v in cities.iteritems():
	print k + " mean = " + str(df[k].mean())
	print k + " range = " + str(df[k].min()) + "-" + str(df[k].max())
	print k + " variance = " + str(df[k].var())

# NewYork mean = 39.0573333333
# NewYork range = 19.72-59.96
# NewYork variance = 113.52619954
# Cleveland mean = 34.2343333333
# Cleveland range = 12.95-59.2
# Cleveland variance = 196.746032299
# Philadelphia mean = 40.2013333333
# Philadelphia range = 17.21-63.85
# Philadelphia variance = 144.545156782
# Denver mean = 37.1713333333
# Denver range = 1.09-58.04
# Denver variance = 161.506991264
# Chicago mean = 30.6353333333
# Chicago range = 6.93-49.86
# Chicago variance = 143.95888092
total_change = collections.defaultdict(int)

# for col in df.columns:
# 	temp_values = df[col].tolist()
# 	temp_change = 0
# 	for k, v in enumerate(temp_values):
# 		if k < len(temp_values) - 1:
# 			temp_change += abs(temp_vals[k] - temp_vals[k+1])
# 	total_change[]