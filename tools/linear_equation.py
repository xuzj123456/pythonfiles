# coding=utf-8
from scipy import linalg
import numpy as np

# x1 + x2 + 7*x3 = 2
# 2*x1 + 3*x2 + 5*x3 = 3
# 4*x1 + 2*x2 + 6*x3 = 4

A = np.array([[1, 1, 7], [2, 3, 5], [4, 2, 6]])  # A代表系数矩阵
b = np.array([2, 3, 4])  # b代表常数列
x = linalg.solve(A, b)
print(x)