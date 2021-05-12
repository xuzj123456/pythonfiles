# coding=utf-8
import pandas as pd
import numpy as np

file = r'E:\微信\新建文件夹\WeChat Files\xisijialouluo\FileStorage\File\2019-12\X13_房地产数据 (2)_2019-12-04 09-49-13.xlsx'
df = pd.read_excel(file, index_col = 0)

def CI(df):
    df = df.dropna()
    df2 = pd.DataFrame(index=df.index)

    A = []
    for c in df.columns:
        if 0<df[c].min()<100 and df[c].max()>100:
            df2[c] = df[c].diff(1)
        else:
            df2[c] = 200 * (df[c] - df[c].shift(1)) / (df[c] + df[c].shift(1))

        A.append(abs(df2[c]).sum()/len(df2[c]))
        df2[c] = df2[c]/A[-1]

    print(df2)
    R = [0]
    W1 = np.ones(df2.shape[1])  # 当前为等权重
    for i in range(1, df2.shape[0]):
        R.append((df2[i:i+1] * W1).sum(axis=1) / np.sum(W1))

    I = [100]
    I.append(I[0]*(200+R[1])/(200-R[1]))
    for i in range(1, df2.shape[0]-1):
        I.append(I[i].values*(200+R[i+1])/(200-R[i+1]))

    return I

Result = CI(df[estate])

i_list_kl = ['中债国债到期收益率:5年','出口价格指数(HS2):总指数',
          'CPI:当月同比.1','消费者预期指数(月)','开放式基金占比','PMI:主要原材料购进价格','人民币:名义有效汇率指数',
          '银行间同业拆借加权利率:1个月','价格:OPEC一揽子石油','全社会用电量:第三产业:累计同比']

i_list2 = ['CPI:当月同比','RPI:当月同比','中债国债到期收益率:1年','零售额:建筑及装潢材料类:累计同比','农业生产资料价格指数:总指数:当月同比',
           '用电量:工业:累计同比','税收收入:累计同比','商品房销售面积:累计同比']

estate = ['房地产开发投资完成额:累计值_log_diff','SHIBOR:1年','中国玻璃价格指数:月',
          '中债国债到期收益率:1年','中债国债到期收益率:5年','通用设备制造业:利润总额:累计同期增减',
          'M2:同比','钢材综合价格指数:月','70个大中城市二手房住宅价格:当月同比:下跌城市数',
          'OECD综合领先指标:五个主要亚洲国家','十大城市:商品房可售套数:一线城市:当月值',
          '出口数量:装载机:主要企业:滑移:累计值','成交量:大连:期货合计:当月同比',
          '对CPI拉动:居住']

estate = ['中债国债到期收益率:1年','中债国债到期收益率:5年','通用设备制造业:利润总额:累计同期增减',
          '出口数量:装载机:主要企业:滑移:累计值','成交量:大连:期货合计:当月同比',
          '房地产开发资金来源:其他资金:个人按揭贷款:累计值_log_diff',
          '十大城市:商品房存销比(面积):一线城市:当月值','十大城市:商品房成交套数:月',
          '十大城市:商品房存销比(套数):一线城市:当月值','30大中城市:商品房成交套数:二线城市:月']

X1 = '70个大中城市二手住宅价格指数:环比'
