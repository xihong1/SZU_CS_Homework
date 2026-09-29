import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

#读入数据
data=sio.loadmat("./MatrixA.mat")
data=data['A']
m,n=data.shape
#初始化QR矩阵的大小
Q=np.zeros((m,n))
R=np.zeros((n,n))
for k in range(n):
    a=data[:,k]
    for i in range(k):
        R[i,k]=np.dot(Q[:,i],a)
        a=a-R[i,k]*Q[:,i]
    #单位化
    R[k,k]=np.linalg.norm(a)
    Q[:,k]=a/R[k,k]

#判断Q矩阵是否正交,考虑到计算机存储偏差设置为1e-6
def is_orthogonal(Q, tolerance=1e-6):
    QTQ=Q.T @ Q
    clean_Q=QTQ
    clean_Q[np.abs(clean_Q) < tolerance] = 0
    I=np.eye(n)
    return np.allclose(clean_Q, I, atol=tolerance)
print("Q的正交性为：",is_orthogonal(Q))
    

#正交性偏差
ek=[]
for i in range(1,n):
    maxe=0
    for j in range(i):
        if maxe<abs(np.dot(Q[:,j],Q[:,i])):
            maxe=abs(np.dot(Q[:,j],Q[:,i]))
    ek.append(maxe)
k=range(2,n+1)
#可视化
plt.plot(k, ek, label='GS_ek')
plt.xlabel('k')
plt.ylabel('ek')
plt.legend()
plt.savefig('GS.png')
plt.show()