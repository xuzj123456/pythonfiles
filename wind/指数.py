# coding=utf-8
from configuration import *


result = w.edb(list_2_code, "2010-01-01", t,"Fill=Previous")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna(inplace=True)
df.set_axis(list_2,axis='columns', inplace=True)

def handle_sql(sql):
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)

for i in range(len(df.index)):
    sql = "INSERT INTO 指数_日 VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(df.index[i],
                                                                                      df.iloc[i:i+1, 0].values[0],
                                                                                      df.iloc[i:i+1, 1].values[0],
                                                                                      df.iloc[i:i+1, 2].values[0],
                                                                                      df.iloc[i:i+1, 3].values[0],
                                                                                      df.iloc[i:i+1, 4].values[0],
                                                                                      df.iloc[i:i+1, 5].values[0])
    handle_sql(sql)
