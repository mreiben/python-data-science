import pandas as pd
import numpy as np
import statsmodels.api as sm
import math

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData.to_csv('loansData_clean.csv', header=True, index=False)

#clean data by removing "months" from the Loan.Length column
loansData['Loan.Length'] = map(lambda x: float(x[0:(len(x)-7)]), loansData['Loan.Length'])
#clean data by removing "%" from the Interest.Rate column
loansData['Interest.Rate'] = map(lambda x: float(x[0:(len(x)-1)]), loansData['Interest.Rate'])
#clean data by selecting the lower range of the FICO.Range column
loansData['FICO.Score'] = map(lambda x: int(x.split("-")[0]), loansData['FICO.Range'])
#create true false column for interest rates below 12
loansData['IR_TF'] = map(lambda x: x < 12, loansData['Interest.Rate'])
#create constant intercept for statsmodel
loansData['Intercept'] = 1


intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Funded.By.Investors']
fico = loansData['FICO.Score']
intercept = loansData['Intercept']

ind_vars = ['Intercept', 'Amount.Funded.By.Investors', 'FICO.Score',]


logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

result = logit.fit()

coeff = result.params

print result.summary()


print coeff[0] #constant intercept
print coeff[1] #a1
print coeff[2] #a2

def logistic_function(ficoScore,loanAmnt):
    logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])
    result = logit.fit()
    coeff = result.params
    px = 1/(1 + math.e**(coeff[0] + coeff[2]*ficoScore + coeff[1]*loanAmnt))
    return px

print logistic_function(750, 10000)
