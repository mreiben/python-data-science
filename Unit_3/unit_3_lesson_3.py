from bs4 import BeautifulSoup
import requests
import re

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content)

# for row in soup('table'):
# 	print row

table = soup('table')[6]

columns = ['Country', 'Year', 'Total', 'Men', 'Women']

rows = table(attrs={'class': 'tcont'})

row_country = rows[0].find_all('td')[0]
row_year = rows[0].find_all('td')[1]
row_total = rows[0].find_all('td')[4]
row_men = rows[0].find_all('td')[7]
row_women = rows[0].find_all('td')[10]

print row_country
print row_year
print row_total
print  row_men
print row_women

