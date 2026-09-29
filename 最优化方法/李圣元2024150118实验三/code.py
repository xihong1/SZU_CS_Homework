import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import time

#下载数据集
data=sio.loadmat('Matrix_A_b.mat')
A=data['A']
b=data['b'].flatten()
print(A.shape)
#直接带入正规矩阵
def least_squares(A, b):
    A_T=A.T
    ATA=A_T.dot(A)
    ATb=A_T.dot(b)
    x_pre=np.linalg.inv(ATA).dot(ATb)
    return x_pre
start=time.time()
x_norm=least_squares(A, b)
end=time.time()
ls_time=end-start
min_axb=np.linalg.norm(A.dot(x_norm)-b)
min_axb=min_axb**2
print(f'正规方程带入求解{min_axb}')


#进行QR分解求解最小二乘法
def least_squares_QR(A, b):
    Q,R=np.linalg.qr(A,mode='reduced')
    QTb=Q.T.dot(b)
    x_qr=np.linalg.inv(R).dot(QTb)
    return x_qr
start=time.time()
x_qr=least_squares_QR(A, b)
end=time.time()
qr_time=end-start
min_qr_axb=np.linalg.norm(A.dot(x_qr)-b)
min_qr_axb=min_qr_axb**2
print(f'正规方程QR带入求解{min_qr_axb}')

# def gradient_descent(A, b,alpha=0.001,max_iter=500000,tol=1e-6):
#     m,n=A.shape
#     x=np.zeros(n)
#     loss_history=[]
#     error_history=[]
#     result_history=[]
#     result_history.append(np.linalg.norm(A.dot(x)-b)**2)
#     for k in range(max_iter):
#         r=A.dot(x)-b
#         #计算损失
#         loss=0.5*np.linalg.norm(r)**2
#         loss_history.append(loss)
#         #计算误差
#         error=np.linalg.norm(x-x_norm)
#         error_history.append(error)
#         #计算梯度
#         grad=A.T.dot(r)
#
#         if np.linalg.norm(grad)<tol:
#             print(f"经历步数{k+1}")
#             break
#         result_history.append(np.linalg.norm(A.dot(x)-b) ** 2)
#         x=x-alpha*grad
#     return x,loss_history,error_history,result_history
#
# # x_gd_1,loss_history_1,error_history_1,result_1=gradient_descent(A, b)
# alpha_list = [ 5e-5, 1e-4, 5e-4, 1e-3, 2e-3]
# # alpha_list=[2e-3]
# gd_result_1={}
# for alpha in alpha_list:
#     x_gd_1,loss_history_1,error_history_1,result_1=gradient_descent(A, b,alpha=alpha)
#     gd_result_1[alpha]=(x_gd_1,loss_history_1,error_history_1,result_1)
#
# plt.figure(figsize=(16,8))
#
# max_len_loss = max([len(gd_result_1[alp][1]) for alp in alpha_list])
# plt.subplot(1,2,1)
# colors = ['r', 'g', 'b', 'orange', 'purple', 'brown']
# for i,alpha in enumerate(alpha_list):
#     loss_hist = gd_result_1[alpha][1]
#     loss_hist_padded = loss_hist + [loss_hist[-1]] * (max_len_loss - len(loss_hist))
#     plt.plot(loss_hist_padded, color=colors[i],label=f'alpha={alpha}')
#
# plt.title('loss function during gradient descent(different alpha)')
# # plt.title('loss function during gradient descent')
# plt.xlabel('iteration')
# plt.ylabel('loss')
# plt.legend(loc='best')
# plt.grid(alpha=0.3)
#
# max_len_error = max([len(gd_result_1[alp][2]) for alp in alpha_list])
# plt.subplot(1,2,2)
# for i,alpha in enumerate(alpha_list):
#     error_hist = gd_result_1[alpha][2]
#     error_hist_padded = error_hist + [error_hist[-1]] * (max_len_loss - len(error_hist))
#     plt.plot(gd_result_1[alpha][2], color=colors[i],label=f'alpha={alpha}')
# plt.title('error during gradient descent(different alpha)')
# # plt.title('error during gradient descent')
# plt.xlabel('iteration')
# plt.ylabel('error')
# plt.legend(loc='best')
# plt.grid(alpha=0.3)
#
# plt.tight_layout()
# plt.savefig('gd_different_alpha.png')
# # plt.savefig('gd_alpha_1.png')
# plt.show()
#
# plt.figure(figsize=(8,8))
# max_len_loss = max([len(gd_result_1[alp][3]) for alp in alpha_list])
# colors = ['r', 'g', 'b', 'orange', 'purple', 'brown']
# for i,alpha in enumerate(alpha_list):
#     result_hist = gd_result_1[alpha][3]
#     result_hist_padded = result_hist + [result_hist[-1]] * (max_len_loss - len(result_hist))
#     plt.plot(result_hist_padded, color=colors[i],label=f'alpha={alpha}')
# plt.title('result during gradient descent(different alpha)')
# # plt.title('result during gradient descent')
# plt.xlabel('iteration')
# plt.ylabel('result')
# plt.legend(loc='best')
# plt.grid(alpha=0.3)
# plt.tight_layout()
# plt.savefig('gd_different_alpha_result.png')
# # plt.savefig('gd_alpha_1_result.png')
# plt.show()
def gradient_descent_noalpha(A, b,max_iter=500000,tol=1e-6):
    m,n=A.shape
    x=np.zeros(n)
    loss_history=[]
    error_history=[]
    result_history=[]
    result_history.append(np.linalg.norm(A.dot(x)-b)**2)
    for k in range(max_iter):
        r=A.dot(x)-b
        #计算损失
        loss=0.5*np.linalg.norm(r)**2
        loss_history.append(loss)
        #计算误差
        error=np.linalg.norm(x-x_norm)
        error_history.append(error)
        #计算梯度
        grad=A.T.dot(r)

        if np.linalg.norm(grad)<tol:
            print(f"经历步数{k+1}")
            break
        result_history.append(np.linalg.norm(A.dot(x)-b) ** 2)
        alpha=np.linalg.norm(grad)**2/np.linalg.norm(A.dot(grad))**2
        x=x-alpha*grad
    return x,loss_history,error_history,result_history

start=time.time()
x_gd_1,loss_history_1,error_history_1,result_1=gradient_descent_noalpha(A, b)
end=time.time()
gd_time=end-start
gd_result_1=(x_gd_1,loss_history_1,error_history_1,result_1)

plt.figure(figsize=(16,8))

plt.subplot(1,2,1)
plt.plot(gd_result_1[1], color='r',label=f'auto_alpha')

plt.title('loss function during gradient descent(auto alpha)')
plt.xlabel('iteration')
plt.ylabel('loss')
plt.legend(loc='best')
plt.grid(alpha=0.3)

plt.subplot(1,2,2)
plt.plot(gd_result_1[2], color='r',label=f'auto_alpha')
plt.title('error during gradient descent(auto alpha)')
plt.xlabel('iteration')
plt.ylabel('error')
plt.legend(loc='best')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('gd_auto_alpha.png')
plt.show()

plt.figure(figsize=(8,8))
plt.plot(gd_result_1[3], color='r',label=f'auto_alpha')
plt.title('result during gradient descent(auto alpha)')
plt.xlabel('iteration')
plt.ylabel('result')
plt.legend(loc='best')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('gd_auto_alpha_result.png')
plt.show()

print(f'正规方程求解运行时间{ls_time} QR求解运行时间{qr_time} 梯度下降求解运行时间{gd_time}')