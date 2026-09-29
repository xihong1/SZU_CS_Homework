import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ===== 乱码修复 =====
chinese_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi']
available_fonts = [f.name for f in fm.fontManager.ttflist]
selected_font = None
for font in chinese_fonts:
    if font in available_fonts:
        selected_font = font
        break

if selected_font:
    plt.rcParams['font.sans-serif'] = [selected_font]
    print(f'使用字体: {selected_font}')
else:
    for f in fm.fontManager.ttflist:
        if any(kw in f.name.lower() for kw in ['hei', 'song', 'kai', 'ming', 'yuan', 'chinese', 'cjk', 'noto']):
            plt.rcParams['font.sans-serif'] = [f.name]
            print(f'使用字体: {f.name}')
            break
    else:
        print('警告：未找到中文字体，可能出现乱码')

plt.rcParams['axes.unicode_minus'] = False

# ===== 创建图形 =====
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# 坐标轴范围：以原点为中心（收紧范围让内容占据更大比例）
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)

# 隐藏刻度和边框
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ===== 四个象限背景色 =====
# QI:   x>0, y>0 → 高探索, 高承诺 → 同一性获得
ax.fill_between([0, 1.0], 0, 1.0, color='#A9DFBF', alpha=0.20)
# QII:  x<0, y>0 → 低探索, 高承诺 → 同一性早闭
ax.fill_between([-1.0, 0], 0, 1.0, color='#AED6F1', alpha=0.20)
# QIII: x<0, y<0 → 低探索, 低承诺 → 同一性扩散
ax.fill_between([-1.0, 0], -1.0, 0, color='#F5B7B1', alpha=0.20)
# QIV:  x>0, y<0 → 高探索, 低承诺 → 同一性延缓
ax.fill_between([0, 1.0], -1.0, 0, color='#F9E79F', alpha=0.20)

# ===== 原点处的坐标轴 =====
ax.axhline(0, color='black', linewidth=1.5)
ax.axvline(0, color='black', linewidth=1.5)

# 箭头
ax.annotate('', xy=(1.05, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))
ax.annotate('', xy=(0, 1.05), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))

# ===== 象限标签（大号字 + 大填充，撑满象限）=====
box_props = dict(boxstyle="round,pad=0.5", alpha=0.90, edgecolor='#444', linewidth=1.8)

# QI (0.5, 0.5):  高探索, 高承诺 → 同一性获得
ax.text(0.5, 0.5, '同一性获得\n(Identity Achievement)\n高探索 · 高承诺',
        ha='center', va='center', fontsize=13, fontweight='bold',
        bbox={**box_props, 'facecolor': '#A9DFBF'})

# QII (-0.5, 0.5): 低探索, 高承诺 → 同一性早闭
ax.text(-0.5, 0.5, '同一性早闭\n(Identity Foreclosure)\n低探索 · 高承诺',
        ha='center', va='center', fontsize=13, fontweight='bold',
        bbox={**box_props, 'facecolor': '#AED6F1'})

# QIII (-0.5, -0.5): 低探索, 低承诺 → 同一性扩散
ax.text(-0.5, -0.5, '同一性扩散\n(Identity Diffusion)\n低探索 · 低承诺',
        ha='center', va='center', fontsize=13, fontweight='bold',
        bbox={**box_props, 'facecolor': '#F5B7B1'})

# QIV (0.5, -0.5): 高探索, 低承诺 → 同一性延缓
ax.text(0.5, -0.5, '同一性延缓\n(Identity Moratorium)\n高探索 · 低承诺',
        ha='center', va='center', fontsize=13, fontweight='bold',
        bbox={**box_props, 'facecolor': '#F9E79F'})

# ===== 坐标轴标注 =====
# x 轴标注（右侧端点）
ax.text(1.08, -0.08, '探索\n(Exploration)', ha='center', va='top',
        fontsize=14, fontweight='bold')
# y 轴标注（顶部端点，无标题所以不冲突）
ax.text(-0.08, 1.08, '承诺\n(Commitment)', ha='center', va='bottom',
        fontsize=14, fontweight='bold', rotation=90)

# ===== 轴端点方向标记 =====
ax.text(1.0, -0.05, '高', ha='center', va='top', fontsize=12, color='#555')
ax.text(-1.0, -0.05, '低', ha='center', va='top', fontsize=12, color='#555')
ax.text(-0.07, 1.0, '高', ha='right', va='center', fontsize=12, color='#555')
ax.text(-0.07, -1.0, '低', ha='right', va='center', fontsize=12, color='#555')

# ===== 保存（无标题）=====
plt.tight_layout(pad=0.5)
output_path = 'marcia_identity_quadrants.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f'已保存: {output_path}')
