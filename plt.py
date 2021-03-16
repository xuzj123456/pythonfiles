# coding=utf-8

"""
import matplotlib.pyplot as plt
plt.figure(figsize = [10,5])
plt.plot(y)
plt.xticks(t, rotation = 20)

from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)

plt.ylabel('\n'.join(dat.columns[-2]), fontsize = 20, fontproperties=font_set, rotation = 'vertical',
           verticalalignment = 'center', horizontalalignment = 'left')
"""

"""
t = [dat.index[i] for i in range(0, len(dat.index), 3)]
import matplotlib.pyplot as plt
plt.figure(figsize = [10,5])
plt.plot(dat[dat.columns[-2]])
plt.xticks(t, rotation = 20)

from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=30)
plt.title(dat.columns[-2], fontproperties=font_set)
"""

'''
import matplotlib.pyplot as plt

plt.figure(1)
plt.subplot(121)
plt.plot(ycle)
plt.subplot(122)
plt.plot(df.lngdp_cycle)
plt.show()
'''