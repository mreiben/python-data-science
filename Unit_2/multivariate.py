import pandas as pd
import numpy as np
import statsmodels.api as sm
import math

loansData = pd.read_csv('LoanStats3b.csv', delimiter=',', dtype=unicode, encoding="utf-8-sig", header=1)
loansData.dropna(inplace=True)

#clean data by removing "%" from the int_rate column
loansData['int_rate'] = map(lambda x: float(str(x)[0:len(str(x))-1]), loansData['int_rate'])

#loansData['annual_inc'] = map(lambda x: float(x), loansData['annual_inc'])

intrate = loansData['int_rate']
income = loansData['annual_inc']
ownership = loansData['home_ownership']

print loansData['annual_inc'][0:10]
print loansData[0:1]

#translate ownership values into integers
homeownership = [4 if x =='OWN' else 3 if x =='MORTGAGE' else 2 if x=='RENT' else 1 if x =='OTHER' else 0 for x in ownership]

inc_own_interaction = [a*b for a,b in zip(income, homeownership)]

print 'income = ', income[0:1]
print 'homeownership = ', homeownership[0]
print 'interaction = ', inc_own_interaction[0]

#model interest rate and annual income
y = np.matrix(intrate).transpose()
x1 = np.matrix(income).transpose()

X = sm.add_constant(x1)
model = sm.OLS(y,X)
f = model.fit()

print 'Intercept: ', f.params[0]
print 'x1 coeff: ', f.params[1]

'''intercept = 14.9672136687, x1 slope = 7.79624230251e-06, so the equation of the line is int_rate = 14.9672136687 + 7.79624230251e-06*annual_inc'''

#add ownership to the model
x2 = np.matrix(homeownership).transpose()
x = np.column_stack([x1,x2])
X = sm.add_constant(x)

model = sm.OLS(y, X)
f = model.fit()
print f.params

print 'Intercept multi: ', f.params[0]
print 'x1(income) coeff: ', f.params[1]
print 'x2(ownership) coeff:', f.params[2]

'''so the equation of the line is int_rate = 15.745017387 + 8.21421524993e-06(income) -3.00908185e-01(ownership)'''

#add interaction between income and ownership
x3 = np.matrix(inc_own_interaction).transpose()
x = no.column_stack([x1,x2,x3])
X = sm.add_constant(x)

model = sm.OLS(y,X)
f = model.fit()
print f.params

'''having issues with the data set, could replace the full lending club data set with the cleaned version from the previous lessons'''