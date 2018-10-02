# coding=utf-8
import numpy
from scipy import optimize

c = numpy.array([32, 60, 0])
A_ub = numpy.array([[25, 40, 0], [30, 15, 20], [50, 60, -20], [0, -1, 1]])
B_ub = numpy.array([12600, 12600, 12600, 0])
res = optimize.linprog(-c, A_ub, B_ub, bounds=((0, None), (0, None), (0, None)))
print(res)
