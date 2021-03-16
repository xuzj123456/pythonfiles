# coding=utf-8
import numpy as np

df['ln_deseason'] = [1.0 for i in range(len(df.index))]
mean = []
for m in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
    item = []
    for i in df.index:
        if str(i).split('-')[1] == m:
            item.append(float(df[df.index == i]['lngdp']))
    mean.append(np.mean(item))

    for i in df.index:
        if str(i).split('-')[1] == m:
            df._set_value(i, 'ln_deseason', df[df.index == i]['lngdp'] - mean[-1])
