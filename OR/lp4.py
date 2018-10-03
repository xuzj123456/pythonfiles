# coding=utf-8
import numpy
from scipy import optimize

c = numpy.array([5, 4])
A_ub = numpy.array([[6, 4], [1, 2], [-1, 1], [0, 1]])
B_ub = numpy.array([24, 6, 1, 1])
res = optimize.linprog(-c, A_ub, B_ub, bounds=((0, None), (0, None)))
print(res)
