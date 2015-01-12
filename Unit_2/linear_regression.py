import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#clean data by removing "months" from the Loan.Length column
loansData['Loan.Length'] = map(lambda x: float(x[0:(len(x)-7)]), loansData['Loan.Length'])
#clean data by removing "%" from the Interest.Rate column
loansData['Interest.Rate'] = map(lambda x: float(x[0:(len(x)-1)]), loansData['Interest.Rate'])

#print loansData['Interest.Rate'][0:5]
#print loansData['Loan.Length'][0:5]
#print loansData[0:5]

#clean data by selecting the lower range of the FICO.Range column
loansData['FICO.Score'] = map(lambda x: int(x.split("-")[0]), loansData['FICO.Range'])

#print loansData['FICO.Score'][0:5]

plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()
plt.close()

#create a scatter matrix comparing each column against the others
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()
plt.close()

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Funded.By.Investors']
fico = loansData['FICO.Score']

# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#put the two columns together to create an input matrix
x = np.column_stack([x1,x2])

#create a linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

#output the results
print 'Coefficients: ', f.params[0:2]
print 'Intercept: ', f.params[2]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared