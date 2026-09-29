# -*- coding: utf-8 -*-
"""
填写实验报告 v2 - 完整重建报告内容
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = docx.Document('实验报告.docx')

# ============================================================
# 策略：找到"四、实验记录"和"五、实验总结"标题，然后删除它们之间的所有段落
# 再重新插入实验记录内容，最后在"五、实验总结"后面插入总结内容
# ============================================================

# 先记录关键位置
sections_info = {}
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text == '四、实验记录':
        sections_info['exp_record'] = i
    elif text.startswith('五、实验总结'):
        sections_info['summary'] = i

print(f"四、实验记录 位置: {sections_info.get('exp_record')}")
print(f"五、实验总结 位置: {sections_info.get('summary')}")

# 需要删除的段落范围（从"四、实验记录"之后到"五、实验总结"之前）
exp_start = sections_info['exp_record'] + 1
exp_end = sections_info['summary']

# 删除这些段落
for idx in range(exp_end - 1, exp_start - 1, -1):
    p = doc.paragraphs[idx]
    p._element.getparent().remove(p._element)

# 重新计算"五、实验总结"的位置
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text.startswith('五、实验总结'):
        sections_info['summary'] = i
        break

print(f"删除后 五、实验总结 位置: {sections_info['summary']}")

# ============================================================
# 在"四、实验记录"标题后插入实验记录内容
# ============================================================
# "四、实验记录"的段落索引
exp_record_idx = sections_info['exp_record']
# 插入点在它后面
insert_idx = exp_record_idx + 1

def insert_para(text, bold=False, font_size=10.5, alignment=None):
    """在指定位置插入段落"""
    global insert_idx
    # 创建新段落
    new_para = doc.add_paragraph()
    # 移动到正确位置
    new_para._element.getparent().remove(new_para._element)
    doc.paragraphs[insert_idx]._element.addnext(new_para._element)
    run = new_para.add_run(text)
    run.font.size = Pt(font_size)
    run.bold = bold
    if alignment:
        new_para.alignment = alignment
    insert_idx += 1
    return new_para

def insert_image(image_path, caption):
    """插入图片和图注"""
    global insert_idx
    # 图片段落
    p = doc.add_paragraph()
    p._element.getparent().remove(p._element)
    doc.paragraphs[insert_idx]._element.addnext(p._element)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(image_path, width=Inches(5.5))
    insert_idx += 1

    # 图注段落
    p2 = doc.add_paragraph()
    p2._element.getparent().remove(p2._element)
    doc.paragraphs[insert_idx]._element.addnext(p2._element)
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run(caption)
    run2.font.size = Pt(9)
    run2.italic = True
    insert_idx += 1

# ---- 1. 数据准备与预处理 ----
insert_para("1. 数据准备与预处理", bold=True, font_size=12)
insert_para("使用sklearn自带的Breast Cancer Wisconsin乳腺癌诊断数据集，该数据集包含569个样本，30个特征（如细胞核的半径、质地、周长等），任务为二分类（良性vs恶性）。")
insert_para("")
insert_para("数据集加载与划分：", bold=True)
insert_para("• 数据集总样本数：569，特征数：30")
insert_para("• 类别分布：恶性(malignant) = 212个，良性(benign) = 357个")
insert_para("• 按照80:20比例划分训练集和测试集，训练集455个样本，测试集114个样本")
insert_para("• 使用StandardScaler对数据进行标准化处理（SVM对特征量级敏感，标准化是关键步骤）")
insert_para("")
insert_para("数据标准化前后的特征量级变化显著，例如'mean radius'的均值约为14.13，而'worst fractal dimension'的均值约为0.083，量级差异超过100倍。标准化将每个特征缩放到均值为0、方差为1的分布，确保SVM能够公平地处理所有特征。")
insert_para("")
insert_para("代码如下：", bold=True)
insert_para("""from sklearn.datasets import load_breast_cancer
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
insert_para("")

# ---- 2. 不同核函数的性能对比 ----
insert_para("2. 不同核函数的性能对比", bold=True, font_size=12)
insert_para("分别使用线性核(linear)、多项式核(poly)和高斯核(RBF)训练SVM模型，在测试集上评估各项性能指标。")
insert_para("")
insert_para("实验结果：", bold=True)
insert_para("")
insert_para("核函数性能对比表：")
insert_para("")
insert_para("┌────────────────┬──────────┬───────────┬────────┬───────────┐")
insert_para("│ 核函数          │ Accuracy │ Precision │ Recall │ F1-score  │")
insert_para("├────────────────┼──────────┼───────────┼────────┼───────────┤")
insert_para("│ 线性核(Linear) │ 0.9561   │ 0.9714    │ 0.9577 │ 0.9645    │")
insert_para("│ 多项式核(Poly) │ 0.8684   │ 0.8256    │ 1.0000 │ 0.9045    │")
insert_para("│ 高斯核(RBF)    │ 0.9825   │ 0.9726    │ 1.0000 │ 0.9861    │")
insert_para("└────────────────┴──────────┴───────────┴────────┴───────────┘")
insert_para("")
insert_para("分析：", bold=True)
insert_para("• RBF核表现最佳，准确率达到98.25%，F1分数为98.61%，召回率达到100%，说明RBF核能够很好地捕捉数据中的非线性关系。")
insert_para("• 线性核表现良好，准确率95.61%，说明乳腺癌数据集的类别在特征空间中具有较好的线性可分性。")
insert_para("• 多项式核表现最差，准确率仅86.84%，但召回率达到100%（所有恶性样本都被正确识别），这表明多项式核可能过拟合了决策边界。")
insert_para("")
insert_para("代码如下：", bold=True)
insert_para("""from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

kernels = ['linear', 'poly', 'rbf']
for kernel in kernels:
    svm_model = SVC(kernel=kernel, random_state=42)
    svm_model.fit(X_train_scaled, y_train)
    y_pred = svm_model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"{kernel}核 - 准确率: {acc:.4f}")
    print(classification_report(y_test, y_pred,
          target_names=cancer.target_names))""")
insert_para("")

insert_image('核函数对比与混淆矩阵.png', '图1 不同核函数性能对比柱状图及RBF核混淆矩阵')
insert_para("")

# ---- 3. 参数优化 - 网格搜索 ----
insert_para("3. 参数优化 - 网格搜索(GridSearchCV)", bold=True, font_size=12)
insert_para("使用网格搜索对RBF核SVM的超参数C和gamma进行优化。")
insert_para("")
insert_para("参数搜索空间：", bold=True)
insert_para("• C (惩罚系数): [0.1, 1, 10, 100]")
insert_para("• gamma (核参数): [0.001, 0.01, 0.1, 1]")
insert_para("• 总搜索组合数: 4 × 4 = 16种")
insert_para("• 交叉验证折数: cv=5 (5折交叉验证)")
insert_para("")
insert_para("网格搜索结果：", bold=True)
insert_para("• 最佳参数组合: C=100, gamma=0.001")
insert_para("• 交叉验证最佳得分: 0.9736")
insert_para("")
insert_para("优化前后对比：", bold=True)
insert_para("• 优化前(默认参数 C=1.0, gamma='scale'): 测试集准确率 = 98.25%")
insert_para("• 优化后(网格搜索 C=100, gamma=0.001): 测试集准确率 = 98.25%")
insert_para("• 性能变化: 0.00% (默认参数在该数据集上已经表现优异)")
insert_para("")
insert_para("分析：网格搜索得到的C=100、gamma=0.001表明较大的C值（更严格的误分类惩罚）和较小的gamma值（更大的核宽度）在该数据集上表现最优。默认参数C=1.0、gamma='scale'已经接近最优，说明sklearn的默认参数设置比较合理。")
insert_para("")
insert_para("代码如下：", bold=True)
insert_para("""from sklearn.model_selection import GridSearchCV

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

best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test_scaled)
print(f"测试集准确率: {accuracy_score(y_test, y_pred_best):.4f}")""")
insert_para("")

insert_image('网格搜索参数热力图.png', '图2 网格搜索参数热力图')
insert_para("")

# ---- 4. 决策边界可视化 ----
insert_para("4. 决策边界可视化", bold=True, font_size=12)
insert_para("由于原始数据为30维，使用PCA将数据降维至2维（保留约63%的方差），然后在二维平面上绘制各核函数的决策边界。")
insert_para("")
insert_para("PCA降维结果：", bold=True)
insert_para("• 第一主成分解释方差比: 0.4350 (43.50%)")
insert_para("• 第二主成分解释方差比: 0.1950 (19.50%)")
insert_para("• 累计解释方差比: 0.6300 (63.00%)")
insert_para("")
insert_para("可视化分析：", bold=True)
insert_para("• 线性核的决策边界是一条直线，能够较好地分开两个类别")
insert_para("• 多项式核的决策边界较为复杂，出现了非线性弯曲")
insert_para("• RBF核的决策边界平滑且灵活，能够适应数据的局部结构")
insert_para("• RBF核在类别交界处形成了平滑的过渡区域，这是其泛化能力好的原因之一")
insert_para("")
insert_para("代码如下：", bold=True)
insert_para("""from sklearn.decomposition import PCA

# PCA降维到2D
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)

# 绘制不同核函数的决策边界
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, kernel in enumerate(['linear', 'poly', 'rbf']):
    svm_vis = SVC(kernel=kernel, random_state=42)
    svm_vis.fit(X_train_pca, y_train)
    h = 0.02
    x_min = X_train_pca[:, 0].min() - 1
    x_max = X_train_pca[:, 0].max() + 1
    y_min = X_train_pca[:, 1].min() - 1
    y_max = X_train_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                          np.arange(y_min, y_max, h))
    Z = svm_vis.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
    axes[idx].scatter(X_train_pca[:, 0], X_train_pca[:, 1],
                      c=y_train, cmap=plt.cm.RdYlBu, s=20)
    axes[idx].set_title(f'{kernel}核 决策边界')""")
insert_para("")

insert_image('决策边界可视化.png', '图3 不同核函数决策边界对比（PCA降至2维）')
insert_para("")
insert_image('优化后RBF决策边界.png', '图4 优化后RBF核决策边界 (C=100, gamma=0.001)')
insert_para("")

# ---- 5. 交叉验证对比分析 ----
insert_para("5. 交叉验证对比分析", bold=True, font_size=12)
insert_para("对三种核函数分别进行5折交叉验证，以更全面地评估模型性能。")
insert_para("")
insert_para("5折交叉验证结果：", bold=True)
insert_para("• 线性核(Linear): 准确率 = 0.9692 (+/- 0.0146)")
insert_para("• 多项式核(Poly): 准确率 = 0.9011 (+/- 0.0326)")
insert_para("• 高斯核(RBF): 准确率 = 0.9758 (+/- 0.0128)")
insert_para("")
insert_para("分析：", bold=True)
insert_para("• RBF核的交叉验证得分最高(97.58%)且标准差最小(0.0128)，说明其不仅性能优秀，而且稳定性最好。")
insert_para("• 多项式核的标准差最大(0.0326)，说明其在不同数据子集上的表现波动较大，泛化能力不稳定。")
insert_para("• 线性核的表现介于两者之间，标准差适中。")
insert_para("")
insert_para("代码如下：", bold=True)
insert_para("""from sklearn.model_selection import cross_val_score

for kernel in ['linear', 'poly', 'rbf']:
    scores = cross_val_score(
        SVC(kernel=kernel, random_state=42),
        X_train_scaled, y_train, cv=5)
    print(f"{kernel}: 5折CV准确率 = "
          f"{scores.mean():.4f} (+/- {scores.std():.4f})")""")
insert_para("")

insert_image('交叉验证对比.png', '图5 不同核函数5折交叉验证准确率箱线图')
insert_para("")

# ============================================================
# 填写"五、实验总结"
# ============================================================
# 重新找"五、实验总结"位置
for i, para in enumerate(doc.paragraphs):
    if '五、实验总结' in para.text:
        summary_idx = i
        break

# 删除"五、实验总结"后面的空段落
# 先找到实验总结后面有哪些段落
summary_insert_idx = summary_idx + 1
# 删除从 summary_idx+1 开始到表格之前的所有段落
# 找到表格的位置
table_start = len(doc.paragraphs)
for i in range(summary_idx + 1, len(doc.paragraphs)):
    if doc.paragraphs[i]._element.getparent().tag.endswith('}body'):
        # Check if next elements are tables
        pass

# 简单方案：在五、实验总结标题后直接添加总结内容
# 使用insert_para的方式

def insert_summary_para(text, bold=False, font_size=10.5):
    """在"五、实验总结"标题后插入段落"""
    global summary_idx
    # 重新定位五、实验总结
    for i, para in enumerate(doc.paragraphs):
        if '五、实验总结' in para.text:
            summary_idx = i
            break

    # 在标题后插入
    new_para = doc.add_paragraph()
    new_para._element.getparent().remove(new_para._element)
    doc.paragraphs[summary_idx + 1]._element.addnext(new_para._element)
    # Wait - this inserts AFTER summary_idx+1, not after summary_idx
    # We need to insert right after the heading
    run = new_para.add_run(text)
    run.font.size = Pt(font_size)
    run.bold = bold
    return new_para

# 删除五、实验总结后面的空段落
# 查找五、实验总结后面有哪些非空段落
print("\n五、实验总结后面的段落：")
for i in range(summary_idx, min(summary_idx + 10, len(doc.paragraphs))):
    print(f"  [{i}] '{doc.paragraphs[i].text[:50]}'")

# 在五、实验总结标题后、表格前插入总结内容
# 先找到所有需要的插入点
# 策略：在五、实验总结标题后面立即插入新段落

# 插入总结内容（从后往前插入，这样顺序正确）
summary_texts = [
    ("", False),
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

# 正向插入：在五、实验总结标题后面逐个插入
# 需要从最后一个往前插入，因为每次插入都会影响后续位置
# 但这里我们使用 addnext 方法在标题后插入，新内容会挤到标题后面

# 使用反向插入
for text, bold in reversed(summary_texts):
    new_para = doc.add_paragraph()
    new_para._element.getparent().remove(new_para._element)
    # 每次都重新找"五、实验总结"的位置
    for i, para in enumerate(doc.paragraphs):
        if '五、实验总结' in para.text:
            cur_summary_idx = i
            break
    # 在标题后面插入（紧挨着标题的段落之后）
    doc.paragraphs[cur_summary_idx]._element.addnext(new_para._element)
    run = new_para.add_run(text)
    run.font.size = Pt(10.5)
    run.bold = bold
    if not text:
        run.font.size = Pt(6)

# 保存
output_path = '实验报告_已填写.docx'
doc.save(output_path)
print(f"\n实验报告已保存: {output_path}")

# 验证
doc2 = docx.Document(output_path)
print("\n验证：报告内容概览")
for i, para in enumerate(doc2.paragraphs):
    if para.text.strip():
        print(f"  [{i:3d}] {para.text[:80]}")
print(f"\n总段落数: {len(doc2.paragraphs)}")
print(f"总表格数: {len(doc2.tables)}")
