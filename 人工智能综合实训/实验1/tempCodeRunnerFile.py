demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="上传图片"),
    outputs=gr.Label(num_top_classes=2, label="识别结果"),
    title="猫狗识别器（ResNet50）",
    description="上传一张猫或狗的照片，模型将使用预训练的 ResNet50 判断类别。",
)

if __name__ == "__main__":
    demo.launch()