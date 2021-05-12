# coding=utf-8
from configuration import *

day_lag = 250
X_table = '指数换手率_日'
X_name = '换手率_沪深300指数'
Y_table = '沪深300'
Y_name = '250日涨跌幅'
Y_name_p = '收盘价'

def plot_(df, day_lag):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(df.iloc[:,0], linewidth=1.5, color='r', label=df.columns[0])
    ax2 = ax1.twinx()

    plot2 = ax2.plot(df.iloc[:,1], linewidth=0.8, color='b', label=df.columns[1]+'(t-'+str(day_lag)+')')
    lines = plot1 + plot2
    plt.legend(lines, [l.get_label() for l in lines])


def run(day_lag, X_table, X_name, Y_table, Y_name):
    result = engine.execute("SELECT 日期,{0} FROM stock_index.{1};".format(Y_name, Y_table)).fetchall()
    df = pd.DataFrame(result)
    df.set_index(df[0], inplace=True)
    df.drop(labels=0, axis=1, inplace=True)
    df.columns = [Y_table +' '+ Y_name]

    result = engine.execute("SELECT 日期,{0} FROM emotions.{1};".format(X_name, X_table)).fetchall()
    df_ = pd.DataFrame(result)
    df_.set_index(df_[0], inplace=True)
    df_.drop(labels=0, axis=1, inplace=True)
    df_.columns = [X_name]

    df_.shift(day_lag)

    df = df.join(df_, how='left')

    df = df.iloc[-1000:,]

    # 去除异常值
#    df = df[df.iloc[:,0]>=-0.06]
#    df = df[df.iloc[:,1]<=0.1]
#    df = df[df.iloc[:, 1] >= -0.05]

    df.dropna(inplace=True)

#    去趋势
#    pd.DataFrame(detrend(df, axis=0, overwrite_data=True))
    return df


if __name__ == '__main__':
    df = run(day_lag, X_table, X_name, Y_table, Y_name)
    y = df.iloc[:,0]
    x = df.iloc[:,1]
    X = sm.add_constant(x)  # 给自变量中加入常数项
    model = sm.OLS(y, X).fit()
    print(model.summary())
    print('corr:', df.corr().iloc[0][1])
    print('beta:', model.params[1])
    print('t:', model.tvalues[1])
    print('R2', model.rsquared)

    plt.plot(x, model.predict(), color='r', linewidth=2)
    plt.scatter(x, y, alpha=0.5)
    plt.xlabel(x.name+'(t-'+str(day_lag)+')')
    plt.ylabel(y.name)

#    df_ = run(day_lag, X_table, X_name, Y_table, Y_name_p)
#    plot_(df_, day_lag)

#    day_lag = 1
#    plot_(run(day_lag, X_table, X_name), day_lag)

# 若为负相关
#    day_lag = 5
#    df = run(day_lag, X_table, X_name)
#    df.iloc[:,1] = -df.iloc[:,1]
#    plot_(df, day_lag)