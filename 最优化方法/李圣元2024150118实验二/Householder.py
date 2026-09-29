import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

#读入数据
data=sio.loadmat("./MatrixA.mat")
data=data['A']
m,n=data.shape
#初始化QR矩阵的大小,确保是浮点类型
R = data.copy().astype(float)
Q = np.eye(m)
for k in range(min(n,m-1)):
    #提取当前列的下半部分
    y=R[k:,k]
    e = np.zeros_like(y)
    sign = 1 if y[0] >= 0 else -1
    w=y+sign*np.linalg.norm(y)*e
    v=w/np.linalg.norm(w)
    # 构造Householder变换矩阵
    H=np.eye(m-k)
    H-=2*np.outer(v, v)
    #更新R
    R[k:,k:]=H@R[k:,k:]
    #更新Q
    H_full=np.eye(m)
    H_full[k:,k:]=H
    Q=Q@H_full
#正交性偏差
ek=[]
for i in range(1,m):
    maxe=0
    for j in range(i):
        if maxe<abs(np.dot(Q[:,j],Q[:,i])):
            maxe=abs(np.dot(Q[:,j],Q[:,i]))
    ek.append(maxe)
k=range(2,m+1)
#可视化
plt.plot(k, ek, label='Householder_ek')
plt.xlabel('k')
plt.ylabel('ek')
plt.legend()
plt.savefig('Householder.png')
plt.show()