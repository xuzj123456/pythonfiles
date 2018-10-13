# coding=utf-8
import numpy
from scipy import optimize
'''
max  Z = 2x1 + 3x2
s.t. x1 + 2x2 <= 4
     x1 + x2 = 3
'''

c = numpy.array([2, 3])
A_ub = numpy.array([[1, 2],])
B_ub = numpy.array([4,])
A_eq = numpy.array([[1, 1],])
B_eq = numpy.array([3])
result = optimize.linprog(-c, A_ub, B_ub, A_eq, B_eq)
print(result)
