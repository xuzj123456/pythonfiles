# coding=utf-8
from configuration import *
# partial least-square method

t=5

Y_table = '沪深300'
Y_name = 'MA'+str(t)
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

df.iloc[:,0]=df.iloc[:,0].shift(-t)
df.dropna(inplace=True)

R = df.iloc[:,0].to_numpy().reshape(-1,1)
X = df.iloc[:,1:].to_numpy()

T = R.shape[0]
N = X.shape[1]

JT = np.identity(T)-1/T*np.ones(T).reshape(-1,1)@np.ones(T).reshape(1,-1)
JN = np.identity(N)-1/T*np.ones(N).reshape(-1,1)@np.ones(N).reshape(1,-1)

S_PLS = X@JN@X.T@JT@R*(1/(R.T@JT@X@JN@X.T@JT@R))@R.T@JT@R

S = pd.DataFrame(S_PLS, index=df.index, columns=['情绪指数'])
S = S.join(df.iloc[:,0], how='left')

S_=detrend(S, axis=0, overwrite_data=False)
S_=pd.DataFrame(S_, index=S.index, columns=S.columns)

def plot_(df,s):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(df.iloc[:,0], linewidth=1.2, color='r', label=df.columns[0])
    ax2 = ax1.twinx()

    plot2 = ax2.plot(df.iloc[:,1], linewidth=0.8, color='b', label=df.columns[1]+s)
    lines = plot1 + plot2
    plt.legend(lines, [l.get_label() for l in lines])

print(S_.corr().iloc[0][1])

plot_(S_, '(t+'+str(t)+')')
