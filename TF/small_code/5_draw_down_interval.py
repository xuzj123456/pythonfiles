# coding=utf-8
import pandas as pd

df = pd.read_csv('量道CTA精选1号.csv', index_col=0)

def max_drawdown(df):
    interval = [0, 0]
    max_drawdown_ratio = 0
    for e, i in enumerate(df.iloc[:,0].values):
        for f, j in enumerate(df.iloc[:,0].values):
            if f > e and float(j - i) / i < max_drawdown_ratio:
                max_drawdown_ratio = float(j - i) / i
                interval = [df.index[e], df.index[f]]
    if interval[0] == interval[1]:
        print('No draw down interval')
        return None, 0
    else:
        return interval, max_drawdown_ratio

def max_drawdown_trim(df):
    interval = [0, 0]
    max_drawdown_ratio = 0
    for e, i in enumerate(df.iloc[:,0].values):
        for f, j in enumerate(df.iloc[:,0].values):
            if f > e and float(j - i) / i < max_drawdown_ratio:
                max_drawdown_ratio = float(j - i) / i
                interval = [e, f]
    if interval[0] == interval[1]:
        print('No draw down interval')
        return None, 0, df
    else:
        gap = df.iloc[interval[0]]-df.iloc[interval[1]]
        for i in range(interval[1], len(df.index)):
            df.iloc[i,0] += gap
        df2 = df.drop(index=df.iloc[interval[0]:interval[1], ].index)
        return [df.index[interval[0]], df.index[interval[1]]], max_drawdown_ratio, df2

intervals = []
rates = []
for i in range(5):
    interval, rate, df = max_drawdown_trim(df)
    intervals.append(interval)
    rates.append(rate)

print("五大回测区间:")
for i in range(5):
    print(intervals[i], '   回撤率为：', rates[i])