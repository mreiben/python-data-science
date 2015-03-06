import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from os.path import expanduser

home = expanduser("~")

grade_path = home + "/Dropbox/Coding/python-data-science/Eiben_StoredGrades_WithSectionID.csv"
regents_path = home + "/Dropbox/Coding/python-data-science/Eiben_RegentsScores.csv"
#assignments_path = home + "/Dropbox/Coding/python-data-science/Assignments_All.csv"

#load csv
gradeData = pd.read_csv(grade_path)
regentsData = pd.read_csv(regents_path)
#assignmentsData = pd.read_csv(assignments_path)

#determine column titles
# print list(regentsData.columns.values)

gradeData['PERIOD'] = gradeData['PERIOD'].astype(str)

#clean the gradeData PERIOD column to isolate period digits
for i, v in gradeData['PERIOD'].iteritems():
    if v[0] == "P":
        gradeData['PERIOD'][i] = v[1:2]
    elif (v[1] == "(" or v[1] == "-"):
        gradeData['PERIOD'][i] = v[0:1]
    elif v[1] != "(":
        gradeData['PERIOD'][i] = v[0:2]

gradeData = gradeData[gradeData.PERIOD != 'na']
gradeData = gradeData[gradeData.EXCLUDE_FROM_GPA != "Exclude from GPA"]
gradeData = gradeData[gradeData.STORECODE == 'Y1']
gradeData['PERIOD'] = gradeData['PERIOD'].astype(int)

#print list(gradeData.columns.values)

# a = pd.scatter_matrix(gradeData, alpha=0.05, figsize=(10,10), diagonal='hist')
# plt.show()
# plt.close()

period = gradeData['PERIOD']
percent = gradeData['PERCENT']

#The dependent variable
y = np.matrix(percent).transpose()

#the independent variable
x = np.matrix(period).transpose()

X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()

print f.params

gradeData1 = gradeData[gradeData.PERIOD == 1]
print gradeData1.describe() #percent mean: 78, std: 
gradeData1 = gradeData1['PERCENT'].values
# plt.hist(gradeData1, alpha=0.5, label='1st Period')
plt.hist(gradeData1, weights=np.zeros_like(gradeData1) + 100. / gradeData1.size, alpha=0.5, label='1st Period')

gradeData5 = gradeData[gradeData.PERIOD == 5]
#print gradeData5.describe() # percent mean: 78.14, std: 10.56
gradeData5 = gradeData5['PERCENT'].values
# plt.hist(gradeData5, alpha=0.5, label='5th Period')
plt.hist(gradeData5, weights=np.zeros_like(gradeData5) + 100. / gradeData5.size, alpha=0.5, label='5th Period')

gradeData8 = gradeData[gradeData.PERIOD == 8]
print gradeData8.describe() # percent mean: 77, std: 10.36
gradeData8 = gradeData8['PERCENT'].values
# plt.hist(gradeData8, alpha=0.5, label='8th Period')
plt.hist(gradeData8, weights=np.zeros_like(gradeData8) + 100. / gradeData8.size, alpha=0.5, label='8th Period')

plt.legend(loc='upper left')
plt.xlabel('Score')
plt.ylabel('Frequency')

plt.show()
plt.close()
