import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.naive_bayes import GaussianNB

weightData = pd.read_csv('ideal_weight.csv')

#remove single quotes from column names
weightData.columns = ['id', 'sex', 'actual', 'ideal', 'diff']

#remove single quotes from the 'sex' column
weightData['sex'] = map(lambda x: x[1:(len(x)-1)], weightData['sex'])

#plot the distributions of actual weight and ideal weight
actual = weightData['actual']
ideal = weightData['ideal']

# plt.hist(actual, alpha=0.5)
# plt.hist(ideal, alpha=0.5)
# plt.show()
# plt.close()

#plot the difference between ideal and actual weight
diff = weightData['diff']

# plt.hist(diff)
# plt.show()
# plt.close()

#map 'sex' to a categorical variable
for index, sex in enumerate(weightData['sex']):
	if sex == 'Male':
		weightData['sex'][index] = 0
	elif sex == 'Female':
		weightData['sex'][index] = 1

weightData['sex'] = pd.Categorical(weightData['sex'])

# print len(weightData.index) #182 total rows
# print weightData['sex'].value_counts() #female = 119, male = 63
print weightData[0:4]

data = weightData[['actual', 'ideal', 'diff']]
target = weightData['sex']

clf = GaussianNB()
y_pred = clf.fit(data, target).predict(data)

print ("Number of mislabeled points of a total %d points: %d" %(len(weightData.index), (target != y_pred).sum()))

#Number of mislabeled points of a total 182 points: 14

#predict the sex for actual: 145, ideal: 160, diff: -15
d = {'actual': 145, 'ideal': 160, 'diff': -15}
df = pd.DataFrame(data=d, index[1])
pred = clf.fit(data,target).predict(df)
print(pred)
#0 = male for this data set
