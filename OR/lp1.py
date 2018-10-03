# coding=utf-8
import numpy
from scipy import optimize

target_func = numpy.array([0.2*16000/3, 0.2*16000/3, 0.3*64000/9, 0.3*64000/9, 0.1*32000/9, 0.1*32000/9])
bound_left = numpy.array([[1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1], [16000/3, 0, 64000/9, 0, 32000/9, 0], [0, 16000/3, 0, 64000/9, 0, 32000/9], [0, 0, 0, 0, 32000/9, 32000/9]])
bound_right = numpy.array([0.1, 0.2, 15000, 25000, 100])        # 默认取小于等于号
res = optimize.linprog(-target_func, bound_left, bound_right, bounds=((0, 0.1), (0, 0.2), (0, 0.1), (0, 0.2), (0, 0.1), (0, 0.2)))
# 默认求最小值，求最大值需加-号
print(res)
