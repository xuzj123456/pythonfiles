# coding=utf-8
import numpy as np
def matrixPow(Matrix,n):
    if(type(Matrix)==list):
        Matrix=np.array(Matrix)
    if(n==1):
        return Matrix
    else:
        return np.matmul(Matrix,matrixPow(Matrix,n-1))