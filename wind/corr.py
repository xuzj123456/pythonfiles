# coding=utf-8
from configuration import *

day_lag = 120
X_table = '涨跌停_日'
X_name = '沪深两市涨停家数占比'

def plot_(df, day_lag):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(df.iloc[:,0], linewidth=1.5, color='r', label=df.columns[0])
    ax2 = ax1.twinx()

    plot2 = ax2.plot(df.iloc[:,1], linewidth=0.8, color='b', label=df.columns[1]+'(t-'+str(day_lag)+')')
    lines = plot1 + plot2
    plt.legend(lines, [l.get_label() for l in lines])


def run(day_lag, X_table, X_name):
    Y_table = '沪深300'
    if day_lag in [5, 10, 20, 60, 120, 250]:
        Y_name = 'MA' + str(day_lag)
    elif day_lag == 0:
        Y_name = '收盘价'
    elif day_lag == 1:
        Y_name = 'MA20'
    elif day_lag == 3:
        Y_name = 'MA60'
    elif day_lag == 6:
        Y_name = 'MA120'
    elif day_lag == 12:
        Y_name = 'MA250'

    result = engine.execute("SELECT 日期,{0} FROM emotions.{1};".format(Y_name, Y_table)).fetchall()
    df = pd.DataFrame(result)
    df.set_index(df[0], inplace=True)
    df.drop(labels=0, axis=1, inplace=True)
    df.columns = [Y_table + Y_name]

    result = engine.execute("SELECT 日期,{0} FROM emotions.{1};".format(X_name, X_table)).fetchall()
    df_ = pd.DataFrame(result)
    df_.set_index(df_[0], inplace=True)
    df_.drop(labels=0, axis=1, inplace=True)
    df_.columns = [X_name]

    df_.shift(day_lag)

    df = df.join(df_, how='left')
    df.dropna(inplace=True)

#    若需去趋势则删去注释
#    pd.DataFrame(detrend(df, axis=0, overwrite_data=True))
    return df


if __name__ == '__main__':
    for day_lag in [0, 5, 10, 20, 60, 120, 250]:
#    for day_lag in [0, 1, 3, 6, 12]:
#    for day_lag in [0]:
        df = run(day_lag, X_table, X_name)
        print(df.corr().iloc[0][1])

#    day_lag = 1
#    plot_(run(day_lag, X_table, X_name), day_lag)

# 若为负相关
#    day_lag = 5
#    df = run(day_lag, X_table, X_name)
#    df.iloc[:,1] = -df.iloc[:,1]
#    plot_(df, day_lag)