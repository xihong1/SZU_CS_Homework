import torch
import matplotlib.pyplot as plt
# 定义函数
def target_function(x_val,y_val):
    return (x_val-2)**2+2*(y_val+1)**2+3

 # 优化过程封装
def optimize(optimizer_cls, lr=0.1, momentum=0,alpha=0.9, steps=50):
    x = torch.tensor(10.0, requires_grad=True)  # 初始值x=10
    y = torch.tensor(10.0, requires_grad=True)  # 初始值y=10
    if optimizer_cls.__name__ == "Adam":
        optimizer = optimizer_cls([x, y], lr=lr, betas=(0.9, 0.999))
    elif optimizer_cls.__name__ == "RMSprop":
        optimizer = optimizer_cls([x, y], lr=lr, alpha=alpha)
    else:
        optimizer = optimizer_cls([x, y], lr=lr, momentum=momentum)
    x_history, y_history, loss_history = [], [], []
    for _ in range(steps):
        loss = target_function(x, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        x_history.append(x.item())
        y_history.append(y.item())
        loss_history.append(loss.item())
    return x_history, y_history, loss_history

# 1. 测试不同学习率的SGD
sgd_x1, sgd_y1, sgd_loss1 = optimize(torch.optim.SGD, lr=0.05)
sgd_x2, sgd_y2, sgd_loss2 = optimize(torch.optim.SGD, lr=0.3)
# 2. 测试不同动量的Momentum
momentum_x1, momentum_y1, momentum_loss1 = optimize(torch.optim.SGD, lr=0.1, momentum=0.6)
momentum_x2, momentum_y2, momentum_loss2 = optimize(torch.optim.SGD, lr=0.1, momentum=0.9)
# 3. 测试不同学习率的Adam
adam_x1, adam_y1, adam_loss1 = optimize(torch.optim.Adam, lr=0.01)
adam_x2, adam_y2, adam_loss2 = optimize(torch.optim.Adam, lr=0.5)
# 4. 测试不同衰减率的RMSprop
rmsprop_x1, rmsprop_y1, rmsprop_loss1 = optimize(torch.optim.RMSprop, lr=0.05,alpha=0.8)
rmsprop_x2, rmsprop_y2, rmsprop_loss2 = optimize(torch.optim.RMSprop, lr=0.05,alpha=0.99)

# 绘制结果
plt.figure(figsize=(18, 12))
# SGD不同学习率对⽐
plt.subplot(4, 2, 1)
plt.plot(sgd_loss1, label='SGD lr=0.05')
plt.plot(sgd_loss2, label='SGD lr=0.3')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('SGD with Different Learning Rates')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()
# y值收敛过程对⽐
plt.subplot(4, 2, 2)
plt.plot(sgd_x1, label='SGD lr=0.05')
plt.plot(sgd_x2, label='SGD lr=0.3')
plt.plot(sgd_y1, label='SGD lr=0.05')
plt.plot(sgd_y2, label='SGD lr=0.3')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('x/y Convergence for SGD')
plt.xlabel('Steps')
plt.ylabel('x/y Value')
plt.legend()
#Momentum不同动量对比
plt.subplot(4, 2, 3)
plt.plot(momentum_loss1, label='Momentum=0.6')
plt.plot(momentum_loss2, label='Momentum=0.9')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('Momentum with Different Values')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()
# x/y值收敛过程对比
plt.subplot(4, 2, 4)
plt.plot(momentum_x1, label='x_Momentum=0.6')
plt.plot(momentum_x2, label='x_Momentum=0.9')
plt.plot(momentum_y1, label='y_Momentum=0.6')
plt.plot(momentum_y2, label='y_Momentum=0.9')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('x/y Convergence for Momentum')   
plt.xlabel('Steps')
plt.ylabel('x/y Value')
plt.legend()
# Adam不同学习率对⽐
plt.subplot(4, 2, 5)
plt.plot(adam_loss1, label='Adam lr=0.01')
plt.plot(adam_loss2, label='Adam lr=0.5')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('Adam with Different Learning Rates')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()
# x值收敛过程对⽐
plt.subplot(4, 2, 6)
plt.plot(adam_x1, label='x_Adam lr=0.01')
plt.plot(adam_x2, label='x_Adam lr=0.5')
plt.plot(adam_y1, label='y_Adam lr=0.01')
plt.plot(adam_y2, label='y_Adam lr=0.5')
plt.axhline(y= 2, color='r', linestyle='--', label='Optimal x')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('x/y Convergence for Adam')
plt.xlabel('Steps')
plt.ylabel('x/y Value')
plt.legend()
# RMSprop不同衰减率对比
plt.subplot(4, 2, 7)
plt.plot(rmsprop_loss1, label='RMSprop alpha=0.8')
plt.plot(rmsprop_loss2, label='RMSprop alpha=0.99')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('RMSprop with Different Decay Rates')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()
# x/y值收敛过程对比
plt.subplot(4, 2, 8)
plt.plot(rmsprop_x1, label='x_RMSprop alpha=0.8')
plt.plot(rmsprop_x2, label='x_RMSprop alpha=0.99')
plt.plot(rmsprop_y1, label='y_RMSprop alpha=0.8')
plt.plot(rmsprop_y2, label='y_RMSprop alpha=0.99')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('x/y Convergence for RMSprop')
plt.xlabel('Steps')
plt.ylabel('x/y Value')
plt.legend()


plt.tight_layout()
plt.savefig('实验1-3_optimizer_comparison.png')
plt.show()
print("总结：")
print("1. 学习率过⼩：收敛速度慢，需要更多迭代才能达到最优")
print("2. 学习率过⼤：可能导致震荡，甚⾄发散，⽆法收敛到最优值")
print("3. 动量过⼩：收敛速度较慢，容易陷⼊局部最优")
print("4. 动量过⼤：可能在最优值附近震荡，收敛不稳定")