# coding=utf-8
import statsmodels.api as sm
import pandas as pd
from patsy import dmatrices
import statsmodels

file = r'C:\Users\lenovo\Desktop\cj intern\gdp_final.xls'
df = pd.read_excel(file, index_col=0)



y, X = dmatrices('Lottery ~ Literacy + Wealth + Region', data=df, return_type='dataframe')
mod = sm.OLS(y, X)
res = mod.fit()