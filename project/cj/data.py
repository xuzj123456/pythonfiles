# coding=utf-8
import pandas

def merge(path1, path2):
    dat1 = pandas.read_excel(path1)
    dat2 = pandas.read_excel(path2)
    dat = pandas.merge(dat1, dat2, on="指标名称", how="outer")
    return dat