import torch 

#定义函数
def function_f(x,y):
    return y*x**3+2*x*y**2+5

print("理论推导的偏导数为：")
print("∂f/∂x = 3*y*x**2 + 2*y**2=62")
print("∂f/∂y = x**3 + 4*x*y=51")
#赋值x，y为3.0和2.0，设置requires_grad=True以便计算梯度
x=torch.tensor(3.0, requires_grad=True)
y=torch.tensor(2.0, requires_grad=True)

f=function_f(x,y)
#反向传播计算梯度
f.backward()
print("\nPyTorch⾃动微分结果：")
print(f"df/dx = {x.grad.item()}")
print(f"df/dy = {y.grad.item()}")
# 验证是否与理论值⼀致
print("\n验证结果：")
print(f"df/dx 匹配: {abs(x.grad.item() - 62) < 1e-10}")
print(f"df/dy 匹配: {abs(y.grad.item() - 51) < 1e-10}")
#同上
x=torch.tensor(1.0, requires_grad=True)
y=torch.tensor(4.0, requires_grad=True)

print("理论推导的偏导数为：")
print("∂f/∂x = 3*y*x**2 + 2*y**2=44")
print("∂f/∂y = x**3 + 4*x*y=17")

f=function_f(x,y)
f.backward()
print("\nPyTorch⾃动微分结果：")
print(f"df/dx = {x.grad.item()}")
print(f"df/dy = {y.grad.item()}")
# 验证是否与理论值⼀致
print("\n验证结果：")
print(f"df/dx 匹配: {abs(x.grad.item() - 44) < 1e-10}")
print(f"df/dy 匹配: {abs(y.grad.item() - 17) < 1e-10}")

