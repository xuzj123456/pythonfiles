# coding=utf-8
from configuration import *


result = w.edb(list_3_code, "2015-01-01", t,"Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.fillna(0, inplace=True)
df.set_axis(list_3,axis='columns', inplace=True)
df['上证成交变化']=df.iloc[:,0].diff()
df['深交成交变化']=df.iloc[:,1].diff()
df.dropna(inplace=True)

def handle_sql(sql):
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)

for i in range(len(df.index)):
    sql = "INSERT INTO 市场表现_日 VALUES ('{0}','{1}','{2}','{3}','{4}');".format(df.index[i],
                                                                            df.iloc[i:i+1, 0].values[0],
                                                                            df.iloc[i:i+1, 1].values[0],
                                                                            df.iloc[i:i+1, 2].values[0],
                                                                            df.iloc[i:i+1, 3].values[0])
    handle_sql(sql)
