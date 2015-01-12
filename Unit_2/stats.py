import pandas as pd
from scipy import stats

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

# First, split the string on the newlines
data = data.splitlines()

# Then, split each item in this list on the commas. Return as a list.
data = [i.split(', ') for i in data]


# Now, create a pandas dataframe
column_names = data[0]  # this is the first row
data_rows = data[1::]  # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

# Convert Alcohol and Tobacco columns to float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

alcohol_mean = df['Alcohol'].mean()
alcohol_median = df['Alcohol'].median()
alcohol_mode = stats.mode(df['Alcohol'])

tobacco_mean = df['Tobacco'].mean()
tobacco_median = df['Tobacco'].median()
tobacco_mode = stats.mode(df['Tobacco'])

alcohol_range = max(df['Alcohol']) - min(df['Alcohol'])
alcohol_std = df['Alcohol'].std()
alcohol_var = df['Alcohol'].var()

tobacco_range = max(df['Tobacco']) - min(df['Tobacco'])
tobacco_std = df['Tobacco'].std()
tobacco_var = df['Tobacco'].var()

print("The mean for the Alcohol and Tobacco data set is %s for Alcohol and %s for Tobacco.") % (alcohol_mean, tobacco_mean)
print("The median for the Alcohol and Tobacco data set is %s for Alcohol and %s for Tobacco.") % (alcohol_median, tobacco_median)
print("The mode for the Alcohol and Tobacco data set is %s for Alcohol and %s for Tobacco.") % (alcohol_mode, tobacco_mode)

print("The range for the Alcohol and Tobacco data set is %s for Alcohol and %s for Tobacco.") % (alcohol_range, tobacco_range)
print("The standard variation for the Alcohol and Tobacco data set is %s for Alcohol and %s for Tobacco.") % (alcohol_std, tobacco_std)
print("The variance for the Alcohol and Tobacco data set is %s for Alcohol and %s for Tobacco.") % (alcohol_var, tobacco_var)