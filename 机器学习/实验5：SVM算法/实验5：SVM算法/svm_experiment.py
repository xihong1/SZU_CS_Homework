# -*- coding: utf-8 -*-
"""
SVM算法实验 - 深圳大学机器学习实验5
支持向量机(SVM)分类实验：乳腺癌诊断数据集
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix,
                             ConfusionMatrixDisplay)
from sklearn.decomposition import PCA

# ============================================================
# 一、数据准备与预处理
# ============================================================
print("=" * 60)
print("一、数据准备与预处理")
print("=" * 60)

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target
print(f"数据集形状: {X.shape}")
print(f"特征数量: {X.shape[1]}")
print(f"样本数量: {X.shape[0]}")
print(f"类别标签: {cancer.target_names} (0=恶性, 1=良性)")
print(f"类别分布: 恶性={sum(y==0)}, 良性={sum(y==1)}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\n训练集大小: {X_train.shape[0]}")
print(f"测试集大小: {X_test.shape[0]}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("数据标准化完成 (StandardScaler)")

# ============================================================
# 二、不同核函数的性能对比
# ============================================================
print("\n" + "=" * 60)
print("二、不同核函数的性能对比")
print("=" * 60)

kernels = ['linear', 'poly', 'rbf']
kernel_names = ['线性核 (Linear)', '多项式核 (Poly)', '高斯核 (RBF)']
results = {}

for kernel, name in zip(kernels, kernel_names):
    print(f"\n--- {name} ---")
    svm_model = SVC(kernel=kernel, random_state=42)
    svm_model.fit(X_train_scaled, y_train)
    y_pred = svm_model.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results[kernel] = {
        'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1,
        'y_pred': y_pred, 'model': svm_model
    }

    print(f"准确率 (Accuracy):  {acc:.4f}")
    print(f"精确率 (Precision): {prec:.4f}")
    print(f"召回率 (Recall):    {rec:.4f}")
    print(f"F1分数 (F1-score):  {f1:.4f}")
    print(f"\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=cancer.target_names))

# 对比表格
print("\n--- 核函数性能对比汇总 ---")
comparison_df = pd.DataFrame({
    '核函数': kernel_names,
    'Accuracy': [results[k]['accuracy'] for k in kernels],
    'Precision': [results[k]['precision'] for k in kernels],
    'Recall': [results[k]['recall'] for k in kernels],
    'F1-score': [results[k]['f1'] for k in kernels]
})
print(comparison_df.to_string(index=False))

# 绘制核函数对比图
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 柱状图对比
metrics = ['Accuracy', 'Precision', 'Recall', 'F1-score']
x = np.arange(len(metrics))
width = 0.25
for i, (kernel, name) in enumerate(zip(kernels, kernel_names)):
    values = [results[kernel]['accuracy'], results[kernel]['precision'],
              results[kernel]['recall'], results[kernel]['f1']]
    axes[0].bar(x + i * width, values, width, label=name)

axes[0].set_xlabel('评价指标')
axes[0].set_ylabel('分数')
axes[0].set_title('不同核函数性能对比')
axes[0].set_xticks(x + width)
axes[0].set_xticklabels(metrics)
axes[0].legend()
axes[0].set_ylim(0.9, 1.01)
axes[0].grid(axis='y', alpha=0.3)

# 混淆矩阵 - RBF核
cm = confusion_matrix(y_test, results['rbf']['y_pred'])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=cancer.target_names)
disp.plot(ax=axes[1], cmap='Blues')
axes[1].set_title('RBF核 - 混淆矩阵')

plt.tight_layout()
plt.savefig('核函数对比与混淆矩阵.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n图片已保存: 核函数对比与混淆矩阵.png")

# ============================================================
# 三、参数优化 - 网格搜索
# ============================================================
print("\n" + "=" * 60)
print("三、参数优化 - 网格搜索 (GridSearchCV)")
print("=" * 60)

param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1],
    'kernel': ['rbf']
}

print(f"参数搜索空间:")
print(f"  C: {param_grid['C']}")
print(f"  gamma: {param_grid['gamma']}")
print(f"  总搜索组合数: {len(param_grid['C']) * len(param_grid['gamma'])}")

grid_search = GridSearchCV(
    SVC(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_train_scaled, y_train)

print(f"\n最佳参数组合: {grid_search.best_params_}")
print(f"交叉验证最佳得分: {grid_search.best_score_:.4f}")

best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test_scaled)

acc_before = results['rbf']['accuracy']
acc_after = accuracy_score(y_test, y_pred_best)
prec_after = precision_score(y_test, y_pred_best)
rec_after = recall_score(y_test, y_pred_best)
f1_after = f1_score(y_test, y_pred_best)

print(f"\n--- 优化前后对比 (RBF核) ---")
print(f"优化前 (默认参数):  C=1.0, gamma='scale'")
print(f"  准确率: {acc_before:.4f}")
print(f"优化后 (网格搜索):  C={grid_search.best_params_['C']}, gamma={grid_search.best_params_['gamma']}")
print(f"  准确率: {acc_after:.4f}")
print(f"性能提升: {(acc_after - acc_before) * 100:.2f}%")

print(f"\n优化后分类报告:")
print(classification_report(y_test, y_pred_best, target_names=cancer.target_names))

# 绘制参数热力图
scores = grid_search.cv_results_['mean_test_score']
scores = scores.reshape(len(param_grid['C']), len(param_grid['gamma']))

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(scores, interpolation='nearest', cmap='YlOrRd')
ax.set_xlabel('gamma')
ax.set_ylabel('C')
ax.set_xticks(range(len(param_grid['gamma'])))
ax.set_xticklabels(param_grid['gamma'])
ax.set_yticks(range(len(param_grid['C'])))
ax.set_yticklabels(param_grid['C'])
ax.set_title('网格搜索参数热力图 (交叉验证准确率)')
plt.colorbar(im)

for i in range(len(param_grid['C'])):
    for j in range(len(param_grid['gamma'])):
        text = ax.text(j, i, f'{scores[i, j]:.4f}', ha='center', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('网格搜索参数热力图.png', dpi=150, bbox_inches='tight')
plt.close()
print("图片已保存: 网格搜索参数热力图.png")

# ============================================================
# 四、决策边界可视化
# ============================================================
print("\n" + "=" * 60)
print("四、决策边界可视化")
print("=" * 60)

pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

print(f"PCA降维: {X_train_scaled.shape[1]}维 -> 2维")
print(f"解释方差比: {pca.explained_variance_ratio_}")
print(f"累计解释方差比: {sum(pca.explained_variance_ratio_):.4f}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (kernel, name) in enumerate(zip(['linear', 'poly', 'rbf'], kernel_names)):
    svm_vis = SVC(kernel=kernel, random_state=42)
    svm_vis.fit(X_train_pca, y_train)

    h = 0.02
    x_min, x_max = X_train_pca[:, 0].min() - 1, X_train_pca[:, 0].max() + 1
    y_min, y_max = X_train_pca[:, 1].min() - 1, X_train_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = svm_vis.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
    scatter = axes[idx].scatter(X_train_pca[:, 0], X_train_pca[:, 1],
                                c=y_train, cmap=plt.cm.RdYlBu, edgecolors='k', s=20)
    axes[idx].set_title(f'{name} 决策边界')
    axes[idx].set_xlabel('第一主成分 (PC1)')
    axes[idx].set_ylabel('第二主成分 (PC2)')

plt.tight_layout()
plt.savefig('决策边界可视化.png', dpi=150, bbox_inches='tight')
plt.close()
print("图片已保存: 决策边界可视化.png")

# 优化后RBF核的决策边界
fig, ax = plt.subplots(figsize=(8, 6))
best_params_C = grid_search.best_params_['C']
best_params_gamma = grid_search.best_params_['gamma']
svm_best_vis = SVC(kernel='rbf', C=best_params_C, gamma=best_params_gamma, random_state=42)
svm_best_vis.fit(X_train_pca, y_train)

h = 0.02
x_min, x_max = X_train_pca[:, 0].min() - 1, X_train_pca[:, 0].max() + 1
y_min, y_max = X_train_pca[:, 1].min() - 1, X_train_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = svm_best_vis.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
ax.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train, cmap=plt.cm.RdYlBu, edgecolors='k', s=20)
ax.set_title(f'优化后RBF核决策边界 (C={best_params_C}, gamma={best_params_gamma})')
ax.set_xlabel('第一主成分 (PC1)')
ax.set_ylabel('第二主成分 (PC2)')
plt.tight_layout()
plt.savefig('优化后RBF决策边界.png', dpi=150, bbox_inches='tight')
plt.close()
print("图片已保存: 优化后RBF决策边界.png")

# ============================================================
# 五、五折交叉验证对比
# ============================================================
print("\n" + "=" * 60)
print("五、交叉验证对比分析")
print("=" * 60)

cv_results = {}
for kernel, name in zip(kernels, kernel_names):
    scores_cv = cross_val_score(SVC(kernel=kernel, random_state=42),
                                 X_train_scaled, y_train, cv=5, scoring='accuracy')
    cv_results[kernel] = scores_cv
    print(f"{name}: 5折交叉验证准确率 = {scores_cv.mean():.4f} (+/- {scores_cv.std():.4f})")

# 交叉验证箱线图
fig, ax = plt.subplots(figsize=(8, 5))
cv_data = [cv_results[k] for k in kernels]
bp = ax.boxplot(cv_data, labels=kernel_names, patch_artist=True)
colors = ['#3498db', '#2ecc71', '#e74c3c']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax.set_ylabel('交叉验证准确率')
ax.set_title('不同核函数5折交叉验证准确率对比')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('交叉验证对比.png', dpi=150, bbox_inches='tight')
plt.close()
print("图片已保存: 交叉验证对比.png")

# ============================================================
# 总结输出
# ============================================================
print("\n" + "=" * 60)
print("实验完成! 生成的图片文件:")
print("=" * 60)
print("1. 核函数对比与混淆矩阵.png")
print("2. 网格搜索参数热力图.png")
print("3. 决策边界可视化.png")
print("4. 优化后RBF决策边界.png")
print("5. 交叉验证对比.png")
print("=" * 60)
