# -*- coding: utf-8 -*-
"""
填写实验报告 - 将实验过程、结果和思考填入实验报告.docx
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = docx.Document('实验报告.docx')

# ============================================================
# 修改实验目的（保留原有内容，补充完善）
# ============================================================
# 原有的实验目的已经填写好了，保持不变

# ============================================================
# 在"四、实验记录"部分插入内容
# ============================================================

# 找到"四、实验记录"的位置
target_para_idx = None
for i, para in enumerate(doc.paragraphs):
    if '四、实验记录' in para.text:
        target_para_idx = i
        break

if target_para_idx is None:
    print("未找到'四、实验记录'标题")
    sys.exit(1)

# 在标题之后的空段落位置开始插入内容
# 我们需要在标题后面添加内容

# 定义要插入的内容
content_sections = []

def add_heading_text(text, level=2):
    """添加小标题"""
    content_sections.append(('heading', text, level))

def add_normal_text(text, bold=False):
    """添加正文"""
    content_sections.append(('normal', text, bold))

def add_image_para(image_path, caption=""):
    """添加图片段落"""
    content_sections.append(('image', image_path, caption))

# ---- 实验过程和结果 ----
add_heading_text("1. 数据准备与预处理", level=2)
add_normal_text("使用sklearn自带的Breast Cancer Wisconsin乳腺癌诊断数据集，该数据集包含569个样本，30个特征（如细胞核的半径、质地、周长等），任务为二分类（良性vs恶性）。", bold=False)
add_normal_text("")
add_normal_text("数据集加载与划分：", bold=True)
add_normal_text("• 数据集总样本数：569，特征数：30")
add_normal_text("• 类别分布：恶性(malignant) = 212个，良性(benign) = 357个")
add_normal_text("• 按照80:20比例划分训练集和测试集，训练集455个样本，测试集114个样本")
add_normal_text("• 使用StandardScaler对数据进行标准化处理（SVM对特征量级敏感，标准化是关键步骤）")
add_normal_text("")
add_normal_text("数据标准化前后的特征量级变化显著，例如'mean radius'的均值约为14.13，而'worst fractal dimension'的均值约为0.083，量级差异超过100倍。标准化将每个特征缩放到均值为0、方差为1的分布，确保SVM能够公平地处理所有特征。")
add_normal_text("")
add_normal_text("代码如下：", bold=True)
add_normal_text("""from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 加载数据集
cancer = load_breast_cancer()
X, y = cancer.data, cancer.target
print(f"数据集形状: {X.shape}")  # (569, 30)

# 划分训练集与测试集 (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# SVM 必须进行标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)""")

add_heading_text("2. 不同核函数的性能对比", level=2)
add_normal_text("分别使用线性核(linear)、多项式核(poly)和高斯核(RBF)训练SVM模型，在测试集上评估各项性能指标。", bold=False)
add_normal_text("")
add_normal_text("实验结果：", bold=True)
add_normal_text("")
add_normal_text("核函数性能对比表：")
add_normal_text("")
add_normal_text("┌────────────────┬──────────┬───────────┬────────┬───────────┐")
add_normal_text("│ 核函数          │ Accuracy │ Precision │ Recall │ F1-score  │")
add_normal_text("├────────────────┼──────────┼───────────┼────────┼───────────┤")
add_normal_text("│ 线性核(Linear) │ 0.9561   │ 0.9714    │ 0.9577 │ 0.9645    │")
add_normal_text("│ 多项式核(Poly) │ 0.8684   │ 0.8256    │ 1.0000 │ 0.9045    │")
add_normal_text("│ 高斯核(RBF)    │ 0.9825   │ 0.9726    │ 1.0000 │ 0.9861    │")
add_normal_text("└────────────────┴──────────┴───────────┴────────┴───────────┘")
add_normal_text("")
add_normal_text("分析：", bold=True)
add_normal_text("• RBF核表现最佳，准确率达到98.25%，F1分数为98.61%，召回率达到100%，说明RBF核能够很好地捕捉数据中的非线性关系。")
add_normal_text("• 线性核表现良好，准确率95.61%，说明乳腺癌数据集的类别在特征空间中具有较好的线性可分性。")
add_normal_text("• 多项式核表现最差，准确率仅86.84%，但召回率达到100%（所有恶性样本都被正确识别），这表明多项式核可能过拟合了决策边界。")
add_normal_text("")
add_normal_text("代码如下：", bold=True)
add_normal_text("""from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

kernels = ['linear', 'poly', 'rbf']
for kernel in kernels:
    svm_model = SVC(kernel=kernel, random_state=42)
    svm_model.fit(X_train_scaled, y_train)
    y_pred = svm_model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"{kernel}核 - 准确率: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=cancer.target_names))""")

add_image_para('核函数对比与混淆矩阵.png', '图1 不同核函数性能对比柱状图及RBF核混淆矩阵')

add_heading_text("3. 参数优化 - 网格搜索(GridSearchCV)", level=2)
add_normal_text("使用网格搜索对RBF核SVM的超参数C和gamma进行优化。", bold=False)
add_normal_text("")
add_normal_text("参数搜索空间：", bold=True)
add_normal_text("• C (惩罚系数): [0.1, 1, 10, 100]")
add_normal_text("• gamma (核参数): [0.001, 0.01, 0.1, 1]")
add_normal_text("• 总搜索组合数: 4 × 4 = 16种")
add_normal_text("• 交叉验证折数: cv=5 (5折交叉验证)")
add_normal_text("")
add_normal_text("网格搜索结果：", bold=True)
add_normal_text(f"• 最佳参数组合: C=100, gamma=0.001")
add_normal_text(f"• 交叉验证最佳得分: 0.9736")
add_normal_text("")
add_normal_text("优化前后对比：", bold=True)
add_normal_text("• 优化前(默认参数 C=1.0, gamma='scale'): 测试集准确率 = 98.25%")
add_normal_text("• 优化后(网格搜索 C=100, gamma=0.001): 测试集准确率 = 98.25%")
add_normal_text("• 性能变化: 0.00% (默认参数在该数据集上已经表现优异)")
add_normal_text("")
add_normal_text("分析：网格搜索得到的C=100、gamma=0.001表明较大的C值（更严格的误分类惩罚）和较小的gamma值（更大的核宽度）在该数据集上表现最优。默认参数C=1.0、gamma='scale'已经接近最优，说明sklearn的默认参数设置比较合理。", bold=False)
add_normal_text("")
add_normal_text("代码如下：", bold=True)
add_normal_text("""from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1],
    'kernel': ['rbf']
}

grid_search = GridSearchCV(
    SVC(random_state=42), param_grid, cv=5,
    scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_scaled, y_train)

print(f"最佳参数组合: {grid_search.best_params_}")
print(f"交叉验证最佳得分: {grid_search.best_score_:.4f}")

# 在测试集上评估
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test_scaled)
print(f"测试集准确率: {accuracy_score(y_test, y_pred_best):.4f}")""")

add_image_para('网格搜索参数热力图.png', '图2 网格搜索参数热力图')

add_heading_text("4. 决策边界可视化", level=2)
add_normal_text("由于原始数据为30维，使用PCA将数据降维至2维（保留约63%的方差），然后在二维平面上绘制各核函数的决策边界。", bold=False)
add_normal_text("")
add_normal_text("PCA降维结果：", bold=True)
add_normal_text("• 第一主成分解释方差比: 0.4350 (43.50%)")
add_normal_text("• 第二主成分解释方差比: 0.1950 (19.50%)")
add_normal_text("• 累计解释方差比: 0.6300 (63.00%)")
add_normal_text("")
add_normal_text("可视化分析：", bold=True)
add_normal_text("• 线性核的决策边界是一条直线，能够较好地分开两个类别")
add_normal_text("• 多项式核的决策边界较为复杂，出现了非线性弯曲")
add_normal_text("• RBF核的决策边界平滑且灵活，能够适应数据的局部结构")
add_normal_text("• RBF核在类别交界处形成了平滑的过渡区域，这是其泛化能力好的原因之一")
add_normal_text("")
add_normal_text("代码如下：", bold=True)
add_normal_text("""from sklearn.decomposition import PCA

# PCA降维到2D
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)

# 绘制不同核函数的决策边界
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, kernel in enumerate(['linear', 'poly', 'rbf']):
    svm_vis = SVC(kernel=kernel, random_state=42)
    svm_vis.fit(X_train_pca, y_train)
    # 生成网格点
    h = 0.02
    x_min, x_max = X_train_pca[:, 0].min() - 1, X_train_pca[:, 0].max() + 1
    y_min, y_max = X_train_pca[:, 1].min() - 1, X_train_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                          np.arange(y_min, y_max, h))
    Z = svm_vis.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
    axes[idx].scatter(X_train_pca[:, 0], X_train_pca[:, 1],
                      c=y_train, cmap=plt.cm.RdYlBu, s=20)
    axes[idx].set_title(f'{kernel}核 决策边界')""")

add_image_para('决策边界可视化.png', '图3 不同核函数决策边界对比（PCA降至2维）')
add_image_para('优化后RBF决策边界.png', '图4 优化后RBF核决策边界 (C=100, gamma=0.001)')

add_heading_text("5. 交叉验证对比分析", level=2)
add_normal_text("对三种核函数分别进行5折交叉验证，以更全面地评估模型性能。", bold=False)
add_normal_text("")
add_normal_text("5折交叉验证结果：", bold=True)
add_normal_text("• 线性核(Linear): 准确率 = 0.9692 (+/- 0.0146)")
add_normal_text("• 多项式核(Poly): 准确率 = 0.9011 (+/- 0.0326)")
add_normal_text("• 高斯核(RBF): 准确率 = 0.9758 (+/- 0.0128)")
add_normal_text("")
add_normal_text("分析：", bold=True)
add_normal_text("• RBF核的交叉验证得分最高(97.58%)且标准差最小(0.0128)，说明其不仅性能优秀，而且稳定性最好。")
add_normal_text("• 多项式核的标准差最大(0.0326)，说明其在不同数据子集上的表现波动较大，泛化能力不稳定。")
add_normal_text("• 线性核的表现介于两者之间，标准差适中。")
add_normal_text("")
add_normal_text("代码如下：", bold=True)
add_normal_text("""from sklearn.model_selection import cross_val_score

for kernel in ['linear', 'poly', 'rbf']:
    scores = cross_val_score(SVC(kernel=kernel, random_state=42),
                              X_train_scaled, y_train, cv=5)
    print(f"{kernel}: 5折CV准确率 = {scores.mean():.4f} (+/- {scores.std():.4f})")""")

add_image_para('交叉验证对比.png', '图5 不同核函数5折交叉验证准确率箱线图')

# ============================================================
# 将内容插入到文档中
# ============================================================

# 在标题后面的段落位置开始插入
insert_pos = target_para_idx + 1

# 遍历所有内容类型，逐个插入
for content_type, text_or_path, extra in content_sections:
    if content_type == 'heading':
        p = doc.paragraphs[insert_pos] if insert_pos < len(doc.paragraphs) else doc.add_paragraph()
        p.clear()
        run = p.add_run(text_or_path)
        run.bold = True
        run.font.size = Pt(12)
        if hasattr(p, 'style') and text_or_path.startswith(('1.', '2.', '3.', '4.', '5.')):
            pass
        insert_pos += 1

    elif content_type == 'normal':
        p = doc.paragraphs[insert_pos] if insert_pos < len(doc.paragraphs) else doc.add_paragraph()
        p.clear()
        run = p.add_run(text_or_path)
        run.font.size = Pt(10.5)
        run.bold = extra  # extra is the bold flag
        if not text_or_path:  # 空行
            run.font.size = Pt(6)
        insert_pos += 1

    elif content_type == 'image':
        # 添加图片
        p = doc.paragraphs[insert_pos] if insert_pos < len(doc.paragraphs) else doc.add_paragraph()
        p.clear()
        try:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run()
            run.add_picture(text_or_path, width=Inches(5.5))
        except Exception as e:
            run = p.add_run(f"[图片: {text_or_path} - {e}]")
        insert_pos += 1

        # 添加图注
        p2 = doc.paragraphs[insert_pos] if insert_pos < len(doc.paragraphs) else doc.add_paragraph()
        p2.clear()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(extra)
        run2.font.size = Pt(9)
        run2.italic = True
        insert_pos += 1

# ============================================================
# 填写五、实验总结
# ============================================================
summary_idx = None
for i, para in enumerate(doc.paragraphs):
    if '五、实验总结' in para.text:
        summary_idx = i
        break

if summary_idx is not None:
    insert_pos = summary_idx + 1

    summary_content = [
        ("本次SVM算法实验使用乳腺癌诊断数据集，系统地完成了支持向量机的分类实验。通过实验，我深入理解了SVM的核心概念，包括超平面、支持向量、核函数以及软间隔的原理。", False),
        ("", False),
        ("主要实验成果：", True),
        ("1. 数据标准化的重要性：由于乳腺癌数据集各特征量级差异很大（如mean radius约14.13，worst fractal dimension约0.083），SVM对特征量级敏感，必须进行标准化处理。经过StandardScaler标准化后，各特征被缩放到均值为0、方差为1的标准正态分布。", False),
        ("2. 核函数对比发现RBF核在该数据集上表现最优（准确率98.25%），线性核次之（95.61%），多项式核表现最差（86.84%）。RBF核能够通过高斯函数将数据映射到高维空间，有效捕捉非线性关系。", False),
        ("3. 网格搜索优化后得到最佳参数C=100、gamma=0.001，但与默认参数相比测试集准确率未发生变化（均为98.25%）。这说明sklearn的默认参数设置（C=1.0, gamma='scale'）已经相当合理。", False),
        ("4. 通过PCA降维和决策边界可视化，直观地观察到三种核函数的分类边界差异：线性核为直线边界，多项式核为复杂曲线边界，RBF核为平滑的非线性边界。", False),
        ("5. 5折交叉验证结果表明RBF核不仅准确率最高（97.58%），而且标准差最小（0.0128），说明其泛化能力和稳定性都是最好的。", False),
        ("", False),
        ("思考题回答：", True),
        ("1. 参数C的作用：当C设置得非常大时，模型倾向于发生过拟合。原因在于C是SVM中惩罚误分类样本的系数，C越大意味着对误分类的惩罚越重。模型会试图正确分类每一个训练样本，导致决策边界变得非常复杂和不规则，过度拟合训练数据中的噪声和细节，从而降低在新数据上的泛化能力。", False),
        ("2. 核函数选择：当样本特征维度n远大于样本数量m时（如基因序列数据），通常推荐使用线性核（Linear Kernel）。原因是：在高维空间中，数据本身已经近似线性可分，使用复杂的非线性核（如RBF）容易导致过拟合；线性核参数少（只有C），计算效率高，不容易过拟合；根据\"维度诅咒\"理论，高维空间中的距离度量变得不可靠，RBF核依赖的距离计算可能失效。", False),
    ]

    for text, bold in summary_content:
        p = doc.paragraphs[insert_pos] if insert_pos < len(doc.paragraphs) else doc.add_paragraph()
        p.clear()
        run = p.add_run(text)
        run.font.size = Pt(10.5)
        run.bold = bold
        if not text:
            run.font.size = Pt(6)
        insert_pos += 1

# 保存文档
output_path = '实验报告_已填写.docx'
doc.save(output_path)
print(f"实验报告已保存: {output_path}")
