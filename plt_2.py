# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False  #用来正常显示负号


file = r'C:\Users\lenovo\Desktop\cj intern\食品饮料.csv'
df = pd.read_csv(file, engine = 'python', index_col=0)
t = [df.index[i] for i in range(0, len(df.index), 6)]

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)

###############################################################

# plt.figure()
# for i in [-11, -8, -7]:
#     plt.plot(df[df.columns[i]], label = df.columns[i])
# plt.legend(markerscale = 10, prop = font_set)
# plt.xticks(t, rotation = 20)

#########################################################################################

t = [df.index[i] for i in range(0, len(df.index), 60)]
fig=plt.figure()
ax1=fig.add_subplot(111)
ax1.plot(df.iloc[:,0], label = '道琼斯指数', color = 'r')
plt.xticks(df.index, rotation = 20)
ax2=ax1.twinx()
ax2.plot(df.iloc[:,1], label = '上证指数')

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
plt.legend(handles1+handles2, labels1+labels2, loc='upper left', prop = font_set)
plt.xticks(t, rotation = 20)

##################################################################################################

fig=plt.figure()
ax1=fig.add_subplot(111)
ax1.plot(dat['CI3'], color = 'r', label = 'leading composite indicator')
ax2=ax1.twinx()
ax2.plot(dat['商品房销售额:累计值_cycle'], color = 'b', label = '商品房销售额')

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
plt.legend(handles1+handles2, labels1+labels2, loc='upper left', prop = font_set)
plt.xticks(t)