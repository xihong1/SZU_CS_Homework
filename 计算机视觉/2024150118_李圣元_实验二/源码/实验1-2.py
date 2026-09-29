import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
# 1. 定义神经⽹络
class CustomNN(nn.Module):
    def __init__(self):
        super(CustomNN, self).__init__()
        self.fc1 = nn.Linear(3, 32)  # 输⼊层→隐藏层
        self.relu = nn.ReLU()        # ReLU激活函数
        self.fc2 = nn.Linear(32, 16)  # 隐藏层→隐藏层
        self.relu = nn.ReLU()        # ReLU激活函数
        self.fc3 = nn.Linear(16, 1)  # 隐藏层→输出层

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x
# 2. 构造随机数据
np.random.seed(42)
torch.manual_seed(42)
num_samples = 1000
X = torch.tensor(np.random.randn(num_samples, 3), dtype=torch.float32)
y = torch.tensor([[2*X[i,0] + 3*X[i,1] - X[i,2]+0.5] for i in range(num_samples)], dtype=torch.float32)
# 3. 初始化模型、损失函数和优化器
model = CustomNN()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)
# 4. 训练循环
epochs = 200
loss_history = []
for epoch in range(epochs):
    # 前向传播
    outputs = model(X)
    loss = criterion(outputs, y)
    # 反向传播和参数更新
    optimizer.zero_grad()  # 清零梯度
    loss.backward()        # 反向传播
    optimizer.step()       # 更新参数
    loss_history.append(loss.item())
    if (epoch+1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}')
# 5. 绘制损失下降曲线
plt.figure(figsize=(10, 4))
plt.plot(range(1, epochs+1), loss_history)
plt.title('Loss Reduction Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True)
plt.savefig('实验1-2_loss_curve.png')
plt.show()
# ⽤新测试输⼊验证⽹络输出
test_inputs = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], 
dtype=torch.float32)
with torch.no_grad():  # 不计算梯度
    predictions = model(test_inputs)
print("\n测试结果：")
for i in range(len(test_inputs)):
    actual = 2*test_inputs[i,0] + 3*test_inputs[i,1] - test_inputs[i,2] + 0.5
    print(f"输⼊: {test_inputs[i].numpy()}, 预测值: {predictions[i].item():.4f}, 实际值: {actual.item()}")