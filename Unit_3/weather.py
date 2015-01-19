import time
import datetime
import requests

cities = { "Chicago": '41.837551,-87.681844',
			"Cleveland": '41.478462,-81.679435',
			"Denver":'39.761850,-104.881105',
			"New York": '40.663619,-73.938589',
			"Philadelphia": '40.009376,-75.133346'
		}

api_key = "d0bf3238797f7efc5cb6a86fd1128d12"

#https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME

start_date = datetime.datetime.now() - datetime.timedelta(days=30)

str_start_date = str(start_date)

parsed_str_start_date = str_start_date[0:10]+"T"+str_start_date[11:19]

print parsed_str_start_date

api_call_chicago = "https://api.forecast.io/forecast/"+api_key+"/"+cities["Chicago"]+","+parsed_str_start_date

print api_call_chicago

r = requests.get(api_call_chicago)

print r.json().keys()