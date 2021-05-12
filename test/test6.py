# coding=utf-8
import numpy as np

np.random.seed(123)
mean = np.array([0, 0])
cov = np.array([[1,-0.15],[-0.15,1]])
loss_list =[]
for x, y in np.random.multivariate_normal(mean=mean, cov=cov, size=10000):
    if x <= -2.91:
        loss = 7.15
    elif x <= -2.75:
        loss = 5.33
    elif x <= -2.18:
        loss = 2.43
    elif x <= -1.49:
        loss = 0.84
    elif x <= 1.53:
        loss = 0
    elif x <= 2.70:
        loss = -0.68
    elif x <= 3.54:
        loss = -1.17
    else:
        loss = -1.85

    if y <= -1.63:
        loss += 6.24
    elif x <= -1.32:
        loss += 1.51
    elif x <= 1.46:
        loss += 0
    elif x <= 2.41:
        loss += -0.82
    elif x <= 2.69:
        loss += -1.25
    elif x <= 3.04:
        loss += -1.60
    elif x <= 3.72:
        loss += -1.85
    else:
        loss += -2.20

    loss_list.append(loss)

print(np.percentile(loss_list,99))