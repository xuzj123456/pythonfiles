# coding=utf-8
from configuration import *

pca = PCA(n_components=2)

t=1

Y_table = '沪深300'
#Y_name = 'MA'+str(t)
Y_name = '收盘价'
result=engine.execute("SELECT 日期,{0} FROM emotions.{1};".format(Y_name,Y_table)).fetchall()
df = pd.DataFrame(result)
df.set_index(df[0],inplace=True)
df.drop(labels=0,axis=1,inplace=True)
df.columns = [Y_table+'.'+Y_name]

X = [['沪深成交总额','市场表现_日'],
     ['沪深两市风险溢价','市盈率_日'],
     ['沪深两市涨停家数占比','涨跌停_日'],
     ['换手率_沪深300指数','指数换手率_日'],
     ['融资融券余额','资金流_日'],
     ['北上资金净流入','资金流_日'],
     ]


def get_X(df, x, table):
    result = engine.execute("SELECT 日期,{0} FROM emotions.{1};".format(x,table)).fetchall()
    df_ = pd.DataFrame(result)
    df_.set_index(df_[0], inplace=True)
    df_.drop(labels=0, axis=1, inplace=True)
    df_.columns = [table + '.' + x]
    df = df.join(df_, how='left')
    return df

for x, table in X:
    df = get_X(df, x, table)

df.dropna(inplace=True)

Y = df.iloc[:,0:1]
X = pca.fit_transform(df.iloc[:,1:], Y)
df_x = pd.DataFrame(X, index=Y.index,columns=['PCA','PCA2'])
Y = Y.join(df_x.iloc[:,0],how='left')

def plot_(df,s=''):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(df.iloc[:,0], linewidth=1.2, color='r', label=df.columns[0])
    ax2 = ax1.twinx()

    plot2 = ax2.plot(df.iloc[:,1], linewidth=0.8, color='b', label=df.columns[1]+s)
    lines = plot1 + plot2
    plt.legend(lines, [l.get_label() for l in lines])

Y.iloc[:,1]=Y.iloc[:,1].shift(t)
plot_(Y,'(t-5)')

print(Y.corr().iloc[0][1])