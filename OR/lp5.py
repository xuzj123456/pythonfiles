# coding=utf-8
import numpy
from scipy import optimize

c = numpy.array([-1, 1, 2])
A_ub = numpy.array([[1, 2, -1], [-2, 4, 2], [2, 3, 1]])
B_ub = numpy.array([20, 60, 50])
res = optimize.linprog(-c, A_ub, B_ub, bounds=((0, None), (0, None), (0, None)))
print(res)
