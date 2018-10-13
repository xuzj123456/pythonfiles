# coding=utf-8
import numpy
from scipy import optimize
'''
max  Z = 50x1 + 25x2 + 20x3 + 40x4
s.t. 2x1 + x2 <= 30
     x3 + 2x4 <= 20
'''

c = numpy.array([50, 25, 20, 40])
A_ub = numpy.array([[2, 1, 0, 0], [0, 0, 1, 2]])
B_ub = numpy.array([30, 20])
result = optimize.linprog(-c, A_ub, B_ub)
print(result)
