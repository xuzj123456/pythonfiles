# coding=utf-8
import numpy

a = numpy.array([[6, 2],
                 [3, 4],
                 [5, 6]])
print(a.argmax())       # 最大值所在位置,但不显示行和列
print(numpy.where(a == a.max()))        # 显示最大值所在位置的行与列

a.shape = (1, 6)
b = a[:, numpy.array([0, 2, 3])]    # 选择指定列

c = numpy.where(b>1, 1, 0)          # 判断b中元素是否大于1，满足返回1，否则返回0

def f(x): return 1 if x > 0 else 0
f = numpy.vectorize(f)
d = f(c)                # 与where效果相同

e = numpy.identity(6)       # 单位阵
print(numpy.linalg.det(e))      # 矩阵行列式

g = numpy.linalg.inv(e)         # 逆矩阵

h = numpy.transpose(a)          # 转置矩阵
j = h @ a          # 矩阵乘法
