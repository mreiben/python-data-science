from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from pandas.io.json import json_normalize
import sqlite3 as lite
import csv
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import math


url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

req = requests.get(url)

soup = BeautifulSoup(req.content)

# for row in soup('table'):
# 	print row

table = soup('table')[6]

columns = ['Country', 'Year', 'Total', 'Men', 'Women']

rows = table(attrs={'class': 'tcont'})

#iterate through the list removing the last 6 rows, which are not countries in the table
# for x in range(0, (len(rows)-6)):
# 	row_country = str(rows[x].find_all('td')[0])
# 	row_country_parsed = re.findall(r"^.*\>(.*)\<.*$", row_country)[0]
# 	print row_country_parsed

con = lite.connect('education.db')
cur = con.cursor()

#the lines below create the table
with con: #create a table in sqlite
	cur.execute('DROP TABLE IF EXISTS school_life_expectancy')
	cur.execute('CREATE TABLE school_life_expectancy ( country_name REAL, year TEXT, total REAL, men REAL, women REAL);')

#insert values into the table
with con:
	for x in range(0, (len(rows)-6)):
		row_country = str(rows[x].find_all('td')[0])
		row_country_parsed = str(re.findall(r"^.*\>(.*)\<.*$", row_country)[0])
		row_year = str(rows[x].find_all('td')[1])
		row_year_parsed = re.findall(r"^.*\>(.*)\<.*$", row_year)[0]
		row_total = str(rows[x].find_all('td')[4])
		row_total_parsed = float(re.findall(r"^.*\>(.*)\<.*$", row_total)[0])
		row_men = str(rows[x].find_all('td')[7])
		row_men_parsed = float(re.findall(r"^.*\>(.*)\<.*$", row_men)[0])
		row_women = str(rows[x].find_all('td')[10])
		row_women_parsed = float(re.findall(r"^.*\>(.*)\<.*$", row_women)[0])
		cur.execute("INSERT INTO school_life_expectancy(country_name, year, total, men, women) VALUES (?, ?, ?, ?, ?)", (row_country_parsed, row_year_parsed, row_total_parsed, row_men_parsed, row_women_parsed))

df = pd.read_sql_query("SELECT * FROM school_life_expectancy", con)

# print "men mean:", df['men'].mean() #12.25806
# print "men median:", df['men'].median() #12
# print "women mean:", df['women'].mean() #12.4516129
# print "women median:", df['women'].median() #13

with con: #create a table in sqlite fpr GDP data
	cur.execute('DROP TABLE IF EXISTS gdp')
	cur.execute('CREATE TABLE gdp ( country_name TEXT, _1999 REAL, _2000 REAL, _2001 REAL, _2002 REAL, _2003 REAL, _2004 REAL, _2005 REAL, _2006 REAL, _2007 REAL, _2008 REAL, _2009 REAL, _2010 REAL );')

with open('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv','rU') as inputFile:
    next(inputFile) # skip the first two lines
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        with con:
        	gdp_values = [line[0], line[42], line[43], line[44], line[45], line[46], line[47], line[48], line[49], line[50], line[51], line[52], line[53]]
        	cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', gdp_values)

#join matching rows from gdp and school_life_expectancy tables
df = pd.read_sql_query('SELECT * FROM gdp INNER JOIN school_life_expectancy ON school_life_expectancy.country_name = gdp.country_name', con)

#add _ to year column to match column titles
df['year'] = map(lambda x: ("_"+str(x)), df['year'])
#select the gdp for the year that school life expectancy was surveyed
df['gdp_year'] = [df[x][i] for i,x in enumerate(df['year'])]

df = df[df['gdp_year'] != '']

#df['gdp_year'] = [float(df[x]) for x in df['gdp_year']]

gdp_year_values = df['gdp_year']
school_life_total = df['total']

# The dependent variable
y = np.matrix(gdp_year_values).transpose()
# The independent variable
x = np.matrix(school_life_total).transpose()

#creat a linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

#output the results
print f.params #-518215765880.76276 58874510310.842545
