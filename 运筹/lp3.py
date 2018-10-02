# coding=utf-8
import numpy
from scipy import optimize

c = numpy.array([800, 3.5, 5, 6, 500, 750, 350])
A_ub = numpy.array([[1.5, 0, 0, 0, 1, 1, 1], [100, 0.6, 1, 0, 20, 35, 10], [50, 0.9, 0, 1, 50, 75, 40]])
B_ub = numpy.array([50.586, 14000, 16000])
res = optimize.linprog(-c, A_ub, B_ub, bounds=((0, None), (0, None), (0, 7000), (0, 8000), (0, None), (0, None), (0, None)))
print(res)
