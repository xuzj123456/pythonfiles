# coding=utf-8
from WindPy import w
import pandas as pd

w.start()
w.isconnected()

result = w.wset("indexconstituent","date=2021-05-13;windcode=000300.SH")
df = pd.DataFrame(result.Data).transpose()

