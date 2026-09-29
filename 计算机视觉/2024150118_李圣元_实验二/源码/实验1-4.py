import torch
import torch.nn as nn
import matplotlib.pyplot as plt


# 1. 定义全连接网络（可指定层数和激活函数）
class DeepNet(nn.Module):
    def __init__(self, num_layers, activation):
        super(DeepNet, self).__init__()
        layers = []
        # 前 num_layers-1 层为隐藏层：10 -> 10
        for _ in range(num_layers - 1):
            layers.append(nn.Linear(10, 10))
            layers.append(activation())
        # 输出层：10 -> 1
        layers.append(nn.Linear(10, 1))
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)


# 2. 计算各层权重的梯度范数
def get_gradient_magnitudes(model, input_tensor):
    model.zero_grad()
    output = model(input_tensor)
    output.backward()
    gradients = []
    for layer in model.layers:
        if isinstance(layer, nn.Linear):
            gradients.append(torch.norm(layer.weight.grad).item())
    return gradients


# 3. 生成随机输入
input_tensor = torch.randn(1, 10, requires_grad=True)

# 4. 不同深度、不同激活函数下的梯度
depths = [3, 5, 7]
activations = {'Sigmoid': nn.Sigmoid, 'ReLU': nn.ReLU}
results = {}

for name, act_fn in activations.items():
    for depth in depths:
        model = DeepNet(depth, act_fn)
        results[(name, depth)] = get_gradient_magnitudes(model, input_tensor)

# 5. 可视化：不同深度、不同激活函数下的梯度大小变化
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for idx, depth in enumerate(depths):
    ax = axes[idx]
    for name in activations:
        grads = results[(name, depth)]
        ax.plot(range(1, len(grads) + 1), grads, 'o-', label=name)
    ax.set_title(f'{depth} layers')
    ax.set_xlabel('Layer')
    ax.set_ylabel('Gradient Norm')
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.savefig('实验1-4_gradient_vanishing_comparison.png')
plt.show()

for depth in depths:
    for name in activations:
        print(f"{name} {depth}层的梯度大小:", results[(name, depth)])
