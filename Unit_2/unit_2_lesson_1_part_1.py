import pandas as pd

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

# First, split the string on the (hidden characters that indicate) newlines
data = data.splitlines() # we could also do data.split('\n')

# Then, split each item in this list on the commas
# the bracketed expression is a list comprehension
data = [i.split(', ') for i in data] 


# Now, convert create a pandas dataframe
column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

print df

# There's no built-in mode method in Python, so we need scipy.stats
from scipy import stats

#Question 1: what are the mean, median, and mode of the set?
# Convert Alcohol and Tobacco columns to float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

df['Alcohol'].mean() 
# 5.4436363636363634
df['Alcohol'].median() 
# 5.63
# If all numbers occur equally often, stats.mode() will return the smallest number
stats.mode(df['Alcohol']) 
# 4.02

df['Tobacco'].mean() 
# 3.6181818181818186
df['Tobacco'].median() 
# 3.53
stats.mode(df['Tobacco']) 
# 2.71


#Question 2: What are the range, variance, and standard deviation of the set?

max(df['Alcohol']) - min(df['Alcohol']) #range is max minus min
# 2.4500000000000002
df['Alcohol'].std() 
# 0.79776278087252406
df['Alcohol'].var() 
# 0.63642545454546284

max(df['Tobacco']) - min(df['Tobacco'])
# 1.8499999999999996
df['Tobacco'].std() 
# 0.59070835751355388
df['Tobacco'].var() 
# 0.3489363636363606