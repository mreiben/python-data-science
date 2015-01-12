import sqlite3 as lite

con = lite.connect('getting_started.db')

# Select all rows and print the result set one row at a time
with con:

  cur = con.cursor()
  # Select and group cities by state, and find the average high temperature for each state ordered descending by average
  cur.execute("SELECT state, AVG(average_high) FROM weather INNER JOIN cities ON name=city GROUP BY state ORDER BY average_high DESC")

  averages = cur.fetchall()

  for state in averages:
      print state
  
#Filtering grouped data
  cur.execute("SELECT state, AVG(average_high) FROM weather INNER JOIN cities ON name=city GROUP BY state HAVING AVG(average_high) > 65 ORDER BY average_high DESC")

  filtered_averages = cur.fetchall()

  for state in filtered_averages:
      print state
