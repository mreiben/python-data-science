import sqlite3 as lite
import pandas as pd

#Connect to the database
con = lite.connect('getting_started.db')

with con:

  cur = con.cursor()
  #Drop tables before entering them again
  cur.execute("DROP TABLE IF EXISTS cities")
  cur.execute("DROP TABLE IF EXISTS weather")

  #Create the cities and weather tables
  cur.execute("CREATE TABLE cities(name text, state text)")
  cur.execute("CREATE TABLE weather(city text, year integer, warm_month text, cold_month text, average_high integer)")

  #Insert data into the tables
  cities_data = (('New York City', 'NY'), ('Boston', 'MA'), ('Chicago', 'IL'), ('Miami', 'FL'), ('Dallas', 'TX'), ('Seattle', 'WA'), ('Portland', 'OR'), ('San Francisco', 'CA'), ('Los Angeles', 'CA'))
  weather_data = (('New York City', 2013, 'July', 'January', 62), ('Boston', 2013, 'July', 'January', 59), ('Chicago', 2013, 'July', 'January', 59), ('Miami', 2013, 'August', 'January', 84), ('Dallas', 2013, 'July', 'January', 77), ('Seattle', 2013, 'July', 'January', 61), ('Portland', 2013, 'July', 'December', 63), ('San Francisco', 2013, 'September', 'December', 64), ('Los Angeles', 2013, 'September', 'December', 75))
  cur.executemany("INSERT INTO cities VALUES(?,?)", cities_data)
  cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather_data)


  #Join the data together - cities with July being the warmest month
  cur.execute("SELECT city, state, warm_month FROM cities INNER JOIN weather ON name=city WHERE warm_month='July'")

  #Load into a pandas DataFrame
  rows = cur.fetchall()
  cols = [desc[0] for desc in cur.description]
  df = pd.DataFrame(rows, columns=cols)

  #Print out the resulting city and state in a full sentence
  city_array = []
  for index, row in df.iterrows():
    entry = row[0] + ", " + row[1]
    city_array.append(entry)
  comma = ", "
  print "The cities that are warmest in July are: " + comma.join(city_array)