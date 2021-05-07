# coding=utf-8
from configuration import *

table_name = '市盈率_日'

try:
    max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
    if not max_date == None:
        start_date = w.tdaysoffset(-1, max_date).Data[0][0]
except:
    pass

# 市盈率_日
list_1 = ['滚动市盈率(TTM)_沪深两市', '上证_A股_平均市盈率',
             '深交所_A股_平均市盈率','市盈率_沪深300','市盈率_申万300指数','10年期国债收益率']
list_1_code = "M0071666,G8324466,G8324479,M0330172,M0049384,M0325687"

result = w.edb(list_1_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna(inplace=True)
df.set_axis(list_1,
            axis='columns', inplace=True)
df.index.name = '日期'
df['沪深两市风险溢价'] = 1/df['滚动市盈率(TTM)_沪深两市']-df['10年期国债收益率']/100

save_(table_name, df)
