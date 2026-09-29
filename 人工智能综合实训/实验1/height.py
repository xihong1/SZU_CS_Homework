# -*- coding: utf-8 -*-
"""
基于 ResNet50 的猫狗识别器（Gradio 版）

原理：
    ResNet50 是 50 层的深度残差网络，在 ImageNet-1K（1000 类）上预训练。
    其中第 151~268 类为各种犬类，第 281~285 类为各种猫类。
    本程序直接复用预训练权重（迁移学习，无需重新训练），
    把 1000 类的输出聚合为「猫 / 狗」两个类别，并用 Gradio 搭建网页界面。
"""

import time
import gradio as gr
import torch
from PIL import Image
from torchvision import models, transforms

weights = models.ResNet50_Weights.IMAGENET1K_V1
model = models.resnet50(weights=weights)
model.eval()

# 有 GPU 就用 GPU，否则退回 CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# ImageNet 的 1000 个类别名称
imagenet_classes = weights.meta["categories"]

DOG_IDX = list(range(151, 269))
CAT_IDX = list(range(281, 286))

transform = transforms.Compose([
    transforms.Resize(256),                    # 短边缩放到 256
    transforms.CenterCrop(224),                # 中心裁剪到 224x224
    transforms.ToTensor(),                     # 转为 Tensor，像素归一化到 [0,1]
    transforms.Normalize(                      # 按 ImageNet 均值/方差标准化
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])
def predict(image: Image.Image):
    if image is None:
        return {"猫": 0.0, "狗": 0.0}
    image = image.convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    time_start = time.time()
    with torch.no_grad():
        outputs = model(input_tensor)
    time_end = time.time()
    probs = torch.softmax(outputs[0], dim=0).cpu()
    cat_prob = float(probs[CAT_IDX].sum())
    dog_prob = float(probs[DOG_IDX].sum())
    total = cat_prob + dog_prob
    if total > 0:
        cat_prob, dog_prob = cat_prob / total, dog_prob / total

    top_idx = int(torch.argmax(probs))
    top_label = imagenet_classes[top_idx]
    print(f"[{time_end - time_start:.3f}s] top1: {top_label} "
          f"| cat={cat_prob:.4f} dog={dog_prob:.4f}")

    return {"猫": cat_prob, "狗": dog_prob}


# ---------------------------- Gradio 界面 ----------------------------
demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="上传图片"),
    outputs=gr.Label(num_top_classes=2, label="识别结果"),
    title="猫狗识别器（ResNet50）",
    description="上传一张猫或狗的照片，模型将使用预训练的 ResNet50 判断类别。",
)

if __name__ == "__main__":
    demo.launch()
