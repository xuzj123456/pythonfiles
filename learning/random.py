# coding=utf-8
import random as r

l = []
for i in range(6):
    num = r.randrange(10)
    l.append(str(num))
l=''.join(l)
sample = r.sample(l, 3)
