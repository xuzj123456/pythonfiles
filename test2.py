from fredapi import Fred
import statsmodels.api as sm
import pandas as pd

file = r'C:\Users\lenovo\Desktop\cj intern\usa_gdp.xls'
dat = pd.read_excel(file, index_col=0)

data = dat['lngdp']

cycle, trend = sm.tsa.filters.hpfilter(Result, lamb = 14400)

Result.to_csv(r'C:\Users\lenovo\Desktop\cj intern\2.csv')

import matplotlib.pyplot as plt
import math


font2 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 20,
}
p = range(11)
p_lambda = [p[i]*math.exp(-p[i])/(1+math.exp(-p[i])) for i in range(11)]
plt.plot(p, p_lambda)
plt.xlabel('p', font2)
plt.ylabel('pλ(p)', font2)