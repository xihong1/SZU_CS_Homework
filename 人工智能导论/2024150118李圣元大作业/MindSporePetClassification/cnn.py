import os
import mindspore as ms
import mindspore.dataset as ds
import mindspore.dataset.vision.c_transforms as CV
import mindspore.dataset.transforms.c_transforms as C
from mindspore import nn, context, ops
from mindspore.common.initializer import XavierUniform
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image

# ---------------------------------------------------------
# 配置
# ---------------------------------------------------------
context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
image_size = 128
batch_size = 32
num_classes = 2
epochs = 30
learning_rate = 0.001

train_dir = "./dataset1/PetImages/train"
val_dir = "./dataset1/PetImages/eval"


def create_dataset(data_dir, training=True):
    dataset = ds.ImageFolderDataset(data_dir, shuffle=training)

    transform_img = [
        CV.Decode(),
        CV.Resize((image_size, image_size)),
        CV.Rescale(1.0 / 255.0, 0.0),
        CV.Normalize(mean=[0.485, 0.456, 0.406],
                     std=[0.229, 0.224, 0.225]),
        CV.HWC2CHW()
    ]

    transform_label = [C.TypeCast(ms.int32)]

    dataset = dataset.map(transform_img, input_columns="image")
    dataset = dataset.map(transform_label, input_columns="label")
    dataset = dataset.batch(batch_size, drop_remainder=training)

    return dataset


train_dataset = create_dataset(train_dir, training=True)
val_dataset = create_dataset(val_dir, training=False)

print(f"训练集大小: {train_dataset.get_dataset_size()} batches")
print(f"验证集大小: {val_dataset.get_dataset_size()} batches")


class CNN(nn.Cell):
    def __init__(self, num_classes=2):
        super(CNN, self).__init__()

        # 特征提取
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1, pad_mode='pad', weight_init=XavierUniform())
        self.bn1 = nn.BatchNorm2d(32)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)

        self.conv2 = nn.Conv2d(32, 64, 3, padding=1, pad_mode='pad', weight_init=XavierUniform())
        self.bn2 = nn.BatchNorm2d(64)

        self.conv3 = nn.Conv2d(64, 128, 3, padding=1, pad_mode='pad', weight_init=XavierUniform())
        self.bn3 = nn.BatchNorm2d(128)

        # 计算全连接层输入大小
        # 128/2/2/2 = 16 (经过3次池化)
        self.fc1 = nn.Dense(128 * 16 * 16, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Dense(256, num_classes)

    def construct(self, x):
        # 第一层
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.pool(x)

        # 第二层
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.pool(x)

        # 第三层
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.pool(x)

        # 展平
        x = x.view(x.shape[0], -1)

        # 全连接层
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x


# 创建模型
model = CNN(num_classes)
loss_fn = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')
optimizer = nn.Adam(model.trainable_params(), learning_rate=learning_rate)
net_with_loss = nn.WithLossCell(model, loss_fn)
train_network = nn.TrainOneStepCell(net_with_loss, optimizer)

for epoch in range(epochs):
    epoch_loss = 0
    batch_count = 0
    # 训练
    model.set_train(True)

    for data in train_dataset.create_dict_iterator():
        images = data["image"]
        labels = data["label"]

        loss = train_network(images, labels)
        epoch_loss += loss.asnumpy()
        batch_count += 1

    avg_loss = epoch_loss / batch_count if batch_count > 0 else 0

    # 验证
    model.set_train(False)
    correct = 0
    total = 0

    for data in val_dataset.create_dict_iterator():
        images = data["image"]
        labels = data["label"]

        outputs = model(images)
        predictions = outputs.argmax(axis=1)

        correct += (predictions == labels).sum().asnumpy()
        total += labels.shape[0]

    accuracy = 100.0 * correct / total if total > 0 else 0
    model.set_train(True)

    print(f"Epoch [{epoch + 1}/{epochs}] 完成, 平均损失: {avg_loss:.4f}, 验证准确率: {accuracy:.2f}%")


# ---------------------------------------------------------
# 新增功能：展示10张图片的预测结果
# ---------------------------------------------------------
def show_predictions(model, val_dir, num_samples=10):
    """
    展示预测结果：从验证集中随机抽取10张图片，显示预测结果和真实标签

    参数：
    - model: 训练好的模型
    - val_dir: 验证集目录
    - num_samples: 展示的图片数量（默认10张）
    """
    print("\n" + "=" * 60)
    print("展示10张测试图片的预测结果")
    print("=" * 60)

    # 确保模型处于推理模式
    model.set_train(False)

    # 类别映射
    class_names = ["猫", "狗"]

    # 收集验证集所有图片路径和标签
    image_paths = []
    true_labels = []

    # 遍历验证集目录
    cat_dir = os.path.join(val_dir, "Cat")
    dog_dir = os.path.join(val_dir, "Dog")

    # 收集猫的图片
    if os.path.exists(cat_dir):
        cat_images = [os.path.join(cat_dir, f) for f in os.listdir(cat_dir)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        image_paths.extend(cat_images)
        true_labels.extend([0] * len(cat_images))  # 猫标签为0

    # 收集狗的图片
    if os.path.exists(dog_dir):
        dog_images = [os.path.join(dog_dir, f) for f in os.listdir(dog_dir)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        image_paths.extend(dog_images)
        true_labels.extend([1] * len(dog_images))  # 狗标签为1

    # 随机选择10张图片
    if len(image_paths) < num_samples:
        print(f"警告：验证集只有 {len(image_paths)} 张图片，将展示所有图片")
        selected_indices = list(range(len(image_paths)))
    else:
        selected_indices = random.sample(range(len(image_paths)), num_samples)

    # 创建2行5列的展示图
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    axes = axes.flatten()  # 展平axes数组方便索引

    # 预测结果统计
    correct_count = 0
    total_count = 0

    # 处理每张图片
    for i, idx in enumerate(selected_indices):
        if i >= 10:  # 只显示前10张
            break

        img_path = image_paths[idx]
        true_label = true_labels[idx]

        try:
            # 读取并预处理图像
            img = Image.open(img_path).convert('RGB')

            # 应用与训练时相同的预处理
            transform = ms.dataset.vision.Compose([
                CV.Resize((image_size, image_size)),
                CV.Rescale(1.0 / 255.0, 0.0),
                CV.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
                CV.HWC2CHW()
            ])

            # 转换为numpy数组并应用转换
            img_np = np.array(img)
            img_tensor = transform(img_np)
            img_tensor = ms.Tensor(img_tensor, dtype=ms.float32).expand_dims(0)  # 添加batch维度

            # 模型预测
            output = model(img_tensor)
            probs = ops.Softmax()(output)
            pred_label = ops.argmax(probs, axis=1).asnumpy()[0]
            confidence = probs.asnumpy()[0][pred_label]

            # 判断预测是否正确
            is_correct = (pred_label == true_label)
            if is_correct:
                correct_count += 1
            total_count += 1

            # 设置边框颜色：正确为绿色，错误为红色
            border_color = 'green' if is_correct else 'red'

            # 在子图中显示图像
            ax = axes[i]
            ax.imshow(img)
            ax.axis('off')

            # 添加标题：显示预测结果、置信度和真实标签
            pred_class = class_names[pred_label]
            true_class = class_names[true_label]

            title_text = f"预测: {pred_class}\n"
            title_text += f"置信度: {confidence:.1%}\n"
            title_text += f"实际: {true_class}"

            # 根据预测是否正确设置标题颜色
            title_color = 'green' if is_correct else 'red'
            ax.set_title(title_text, color=title_color, fontsize=12, fontweight='bold')

            # 添加边框
            for spine in ax.spines.values():
                spine.set_edgecolor(border_color)
                spine.set_linewidth(3)

        except Exception as e:
            print(f"处理图片 {img_path} 时出错: {e}")
            axes[i].axis('off')
            axes[i].set_title("图片加载失败", color='gray')

    for i in range(len(selected_indices), len(axes)):
        axes[i].axis('off')

    # 添加整体标题
    accuracy_percent = (correct_count / total_count * 100) if total_count > 0 else 0
    fig.suptitle(f'CNN猫狗分类预测结果 (准确率: {accuracy_percent:.1f}%)',
                 fontsize=16, fontweight='bold', y=1.02)

    # 调整布局
    plt.tight_layout()
    plt.show()

    print(f"\n预测统计:")
    print(f"总预测数: {total_count}")
    print(f"正确预测: {correct_count}")
    print(f"预测准确率: {accuracy_percent:.1f}%")

# 调用展示函数
show_predictions(model, val_dir, num_samples=10)

# 保存最终模型
model.set_train(False)
try:
    ms.save_checkpoint(model, "cat_dog_cnn_final2.ckpt")
    print("模型保存成功: cat_dog_cnn_final2.ckpt")
except Exception as e:
    print(f"保存模型时出错: {e}")

# 导出为MINDIR格式
print("\n导出为MINDIR格式...")
input_data = np.random.uniform(0.0, 1.0, size=[1, 3, image_size, image_size]).astype(np.float32)
input_tensor = ms.Tensor(input_data, ms.float32)

try:
    mindir_path = "cat_dog_cnn_model.mindir"
    ms.export(model, input_tensor, file_name=mindir_path, file_format="MINDIR")
    print(f"✓ MINDIR模型导出成功: {mindir_path}")
except Exception as e:
    print(f"导出MINDIR时出错: {e}")

print(f"输入形状: {input_tensor.shape}")
print(f"输出类别: {num_classes}")