import docx
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

doc = Document()

# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 标题
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('深 圳 大 学 实 验 报 告')
run.bold = True
run.font.size = Pt(22)
run.font.name = '宋体'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_paragraph()

# 基本信息
info_items = [
    ('课程名称：', '数值计算方法'),
    ('实验项目名称：', '变步长求积、Romberg求积与Gauss求积'),
    ('学院：', '计算机与软件学院'),
    ('专业：', '人工智能卓越班'),
    ('指导教师：', '吴晓群、卯丙'),
    ('报告人：', '李圣元    学号：2024150118     班级：  01'),
    ('实验时间：', '2026年6月17日 -- 2026年6月30日'),
    ('实验报告提交时间：', '2026年6月23日星期二'),
]

for label, value in info_items:
    p = doc.add_paragraph()
    run = p.add_run(label)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    run = p.add_run(value)
    run.font.size = Pt(14)
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph()
run = p.add_run('教务部制')
run.bold = True
run.font.size = Pt(14)

doc.add_page_break()

# ==================== 实验目的与要求 ====================
h = doc.add_heading('实验目的与要求', level=1)
for run in h.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

purposes = [
    '1. 掌握变步长求积、Romberg求积与Gauss求积等公式、算法及其误差估计',
    '2. 理解对应算法的优缺点及其适用范围',
    '3. 编程实现变步长求积、Romberg求积与Gauss求积等算法，并分析误差及其控制机制',
]
for text in purposes:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# ==================== 基本原理与算法 ====================
h = doc.add_heading('基本原理与算法', level=1)
for run in h.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 1. 变步长梯形求积
h2 = doc.add_heading('1. 变步长梯形求积', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

principles_trap = [
    '在区间 [a, b] 上使用梯形公式及复合形式逐次计算积分。首先利用梯形公式可得积分近似值：',
    'T₁ = (b-a)/2 · [f(a) + f(b)]',
    '将[a, b]二等分，取步长h₁ = (b-a)/2，使用n = 2时的复合梯形公式得：',
    'T₂ = T₁/2 + h₁ · f(a + h₁)',
    '如此继续下去，可得变步长梯形求积公式：',
    'T₂ₖ = T₂ₖ₋₁/2 + hₖ · Σf(xᵢ)',
    '根据复合梯形求积公式的余项公式可得误差估计：',
    '|T₂ₖ - T₂ₖ₋₁| ≈ 1/3 · |T₂ₖ - T₂ₖ₋₁|',
    '若预定精度为ε，则当|T₂ₖ - T₂ₖ₋₁| < ε时终止计算。',
]
for text in principles_trap:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 2. 自适应Simpson求积
h2 = doc.add_heading('2. 自适应Simpson求积', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

principles_simp = [
    'Simpson公式具有3次代数精度，其截断误差为O(h⁴)。自适应Simpson求积根据被积函数的局部变化自动调整子区间大小。',
    '核心思想：对区间[a,b]先用复合Simpson公式计算S(整个区间)，再将区间二分为[a,m]和[m,b]分别计算S₁和S₂。',
    '若|S₁ + S₂ - S| < 15·ε，则取S₁ + S₂ + (S₁ + S₂ - S)/15作为近似值；否则对子区间递归执行上述过程。',
    '该方法在函数变化剧烈处自动加密节点，在平滑处使用较少节点，实现了计算效率的最优化。',
]
for text in principles_simp:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 3. Romberg求积
h2 = doc.add_heading('3. Romberg求积', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

principles_rom = [
    'Romberg求积基于Richardson外推技术，利用梯形值的误差渐进展开式逐次消去截断误差的低阶项。',
    '梯形值T(h)具有误差展开：T(h) = I + a₁h² + a₂h⁴ + a₃h⁶ + ...',
    '外推公式：R(k,j) = R(k,j-1) + [R(k,j-1) - R(k-1,j-1)] / (4ʲ - 1)',
    '其中R(k,0)为梯形序列，R(k,1)为Simpson序列，R(k,2)为Cotes序列，对角线R(k,k)即为Romberg近似值。',
    '该方法可将O(h²)的梯形公式加速到任意高阶精度，且收敛速度快，精度高。',
]
for text in principles_rom:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 4. Gauss-Legendre求积
h2 = doc.add_heading('4. Gauss-Legendre求积', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

principles_gl = [
    'Gauss求积公式通过适当地选取节点和求积系数，使求积公式达到最高的代数精度。',
    'n+1个节点的Gauss求积公式具有2n+1次代数精度，远优于等距节点的Newton-Cotes公式。',
    'Legendre多项式Pₙ(x)是区间[-1, 1]上的正交多项式，其n+1个零点即为Gauss-Legendre求积公式的节点。',
    '求积系数为：Aᵢ = 2/[(1-xᵢ²)·P\'ₙ(xᵢ)²]',
    '积分余项：R[f] = 2^(2n+3)·[(n!)⁴]/[(2n+3)·((2n+2)!)³] · f⁽²ⁿ⁺²⁾(ξ)',
    '对于光滑函数，Gauss-Legendre求积呈指数型收敛，以最少的函数求值次数获得最高精度。',
]
for text in principles_gl:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_page_break()

# ==================== 实验过程及内容 ====================
h = doc.add_heading('实验过程及内容', level=1)
for run in h.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 问题描述
h2 = doc.add_heading('1. 问题描述', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

problem_desc = [
    '采用变步长梯形求积、自适应Simpson求积、Romberg求积与Gauss-Legendre求积等算法计算下列积分，要求绝对误差控制在ε = 0.5×10⁻⁶以内：',
    '',
    '目标积分：I = ∫₀^{π/2} cos(x) dx，精确值 I = 1',
    '验证积分：J = ∫₀¹ x² dx，精确值 J = 1/3',
]
for text in problem_desc:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 实验步骤
h2 = doc.add_heading('2. 实验步骤', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

steps = [
    '（1）算法实现：编写变步长梯形求积、自适应Simpson求积、Romberg求积与Gauss-Legendre求积的MATLAB程序',
    '（2）测试验证：使用验证积分∫₀¹ x² dx = 1/3验证各算法程序的正确性',
    '（3）参数设置：精度要求ε = 0.5×10⁻⁶，各算法设定合理的初始参数',
    '（4）运行计算：对目标积分∫₀^{π/2} cos(x) dx进行求解',
    '（5）结果记录：记录迭代过程、最终结果和性能指标，绘制收敛曲线',
]
for text in steps:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 算法伪代码
h2 = doc.add_heading('3. 算法伪代码', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 变步长梯形
h3 = doc.add_heading('3.1 变步长梯形求积算法伪代码', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

trap_code = """Algorithm VariableStepTrapezoid(f, a, b, ε):
Input: f — 被积函数, [a,b] — 积分区间, ε — 精度要求
Output: I — 积分近似值

h ← b − a
T(1) ← h/2 · [f(a) + f(b)]
for k = 1, 2, 3, ... until convergence:
    h ← h/2
    s ← 0
    x ← a + h
    while x < b:
        s ← s + f(x)
        x ← x + 2h
    end while
    T(k+1) ← T(k)/2 + h·s
    if |T(k+1) − T(k)| < ε:
        return T(k+1)
    end if
end for"""
p = doc.add_paragraph(trap_code)
for run in p.runs:
    run.font.name = 'Courier New'
    run.font.size = Pt(10)

# 自适应Simpson
h3 = doc.add_heading('3.2 自适应Simpson求积算法伪代码', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

simp_code = """Algorithm AdaptiveSimpson(f, a, b, ε, max_depth):
Input: f, [a,b], ε, max_depth
Output: I — 积分近似值

Stack ← [(a, b, ε, 0)]    // 栈: [左端, 右端, 容差, 深度]
results ← []

while Stack is not empty:
    (a', b', eps, depth) ← Stack.pop()
    m ← (a' + b')/2
    S_whole ← (b'−a')/6 · [f(a') + 4f(m) + f(b')]
    S_left  ← (m−a')/6 · [f(a') + 4f((a'+m)/2) + f(m)]
    S_right ← (b'−m)/6 · [f(m) + 4f((m+b')/2) + f(b')]
    S ← S_left + S_right
    
    if depth ≥ max_depth OR |S − S_whole| < 15·eps:
        results.append(S + (S − S_whole)/15)
    else:
        Stack.push((m, b', eps/2, depth+1))
        Stack.push((a', m, eps/2, depth+1))
    end if
end while
return sum(results)"""
p = doc.add_paragraph(simp_code)
for run in p.runs:
    run.font.name = 'Courier New'
    run.font.size = Pt(10)

# Romberg
h3 = doc.add_heading('3.3 Romberg求积算法伪代码', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

rom_code = """Algorithm RombergQuad(f, a, b, ε, max_iter):
Input: f, [a,b], ε, max_iter
Output: I — 积分近似值

h ← b − a
R(1,1) ← h/2 · [f(a) + f(b)]
for k = 1, 2, ..., max_iter:
    h ← h/2
    s ← 0; x ← a + h
    while x < b:
        s ← s + f(x); x ← x + 2h
    end while
    R(k+1, 1) ← R(k,1)/2 + h·s
    
    for j = 1 to k:
        R(k+1, j+1) ← R(k+1,j) + [R(k+1,j) − R(k,j)] / (4^j − 1)
    end for
    
    if |R(k+1,k+1) − R(k,k)| < ε:
        return R(k+1, k+1)
    end if
end for"""
p = doc.add_paragraph(rom_code)
for run in p.runs:
    run.font.name = 'Courier New'
    run.font.size = Pt(10)

# Gauss-Legendre
h3 = doc.add_heading('3.4 Gauss-Legendre求积算法伪代码', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

gl_code = """Algorithm GaussLegendre(f, a, b, n):
Input: f, [a,b], n — 节点数
Output: I — 积分近似值

for i = 1 to n/2 (向上取整):
    x ← cos(π·(4i−3)/(4n+2))      // 初始猜测
    repeat:
        P ← LegendreP(n, x)       // 计算Legendre多项式
        dP ← LegendreP'(n, x)     // 计算导数
        dx ← −P/dP
        x ← x + dx
    until |dx| < 1e-14
    
    nodes(i) ← x;  nodes(n+1−i) ← −x
    weights(i) ← 2/[(1−x²)·dP²]
    weights(n+1−i) ← weights(i)
end for

// 变换到实际区间 [a,b]
x_gl ← (b−a)/2 · nodes + (a+b)/2
w_gl ← (b−a)/2 · weights
I ← Σ w_gl(i) · f(x_gl(i))"""
p = doc.add_paragraph(gl_code)
for run in p.runs:
    run.font.name = 'Courier New'
    run.font.size = Pt(10)

doc.add_page_break()

# ==================== 程序设计 ====================
h = doc.add_heading('程序设计（MATLAB代码）', level=1)
for run in h.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 读取MATLAB代码文件
code_files = {
    '变步长梯形求积函数 (varstep_trapezoid.m)': 'varstep_trapezoid.m',
    '自适应Simpson求积函数 (adaptive_simpson_main.m)': 'adaptive_simpson_main.m',
    'Romberg求积函数 (romberg_quad.m)': 'romberg_quad.m',
    'Gauss-Legendre节点权重 (gauss_legendre_nodes.m)': 'gauss_legendre_nodes.m',
    'Legendre多项式 (legendre_poly.m)': 'legendre_poly.m',
    '主测试程序 (exp14_main.m)': 'exp14_main.m',
}

base_dir = r'D:\课件\数值计算方法\实验14'

for title_text, filename in code_files.items():
    h2 = doc.add_heading(title_text, level=2)
    for run in h2.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        p = doc.add_paragraph(code)
        for run in p.runs:
            run.font.name = 'Courier New'
            run.font.size = Pt(9)

doc.add_page_break()

# ==================== 实验结果与分析 ====================
h = doc.add_heading('实验结果与分析', level=1)
for run in h.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 结果展示
h2 = doc.add_heading('1. 实验结果展示', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

p = doc.add_paragraph('表1  目标积分计算结果汇总（ε = 0.5×10⁻⁶，精确值 = 1）')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.bold = True
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 表1
table1 = doc.add_table(rows=5, cols=5)
table1.style = 'Table Grid'
table1.alignment = WD_TABLE_ALIGNMENT.CENTER

headers1 = ['求积方法', '近似值', '绝对误差', '迭代次数', '函数调用数']
data1 = [
    ['变步长梯形', '0.999999950977142', '4.90×10⁻⁸', '11', '2049'],
    ['自适应Simpson', '0.999999999421199', '5.79×10⁻¹⁰', '3', '~40'],
    ['Romberg', '0.999999999998017', '1.98×10⁻¹²', '4', '31'],
    ['Gauss-Legendre(n=5)', '1.000000000039559', '3.96×10⁻¹¹', '5', '5'],
]

for j, header in enumerate(headers1):
    cell = table1.rows[0].cells[j]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)
            run.font.name = '宋体'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

for i, row_data in enumerate(data1):
    for j, val in enumerate(row_data):
        cell = table1.rows[i+1].cells[j]
        cell.text = val
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(10)
                run.font.name = '宋体'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_paragraph()

p = doc.add_paragraph('表2  验证积分计算结果（精确值 = 1/3 ≈ 0.333333333333333）')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.bold = True
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 表2
table2 = doc.add_table(rows=5, cols=3)
table2.style = 'Table Grid'
table2.alignment = WD_TABLE_ALIGNMENT.CENTER

headers2 = ['求积方法', '近似值', '绝对误差']
data2 = [
    ['变步长梯形', '0.333333492279053', '1.59×10⁻⁷'],
    ['自适应Simpson', '0.333333333333333', '< 10⁻¹⁵'],
    ['Romberg', '0.333333333333333', '< 10⁻¹⁵'],
    ['Gauss-Legendre(n=5)', '0.333333333333332', '1.11×10⁻¹⁵'],
]

for j, header in enumerate(headers2):
    cell = table2.rows[0].cells[j]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)
            run.font.name = '宋体'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

for i, row_data in enumerate(data2):
    for j, val in enumerate(row_data):
        cell = table2.rows[i+1].cells[j]
        cell.text = val
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(10)
                run.font.name = '宋体'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_paragraph()

p = doc.add_paragraph('表3  Romberg求积T表（被积函数cos(x)，区间[0, π/2]）')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.bold = True
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 表3 - Romberg T表
table3 = doc.add_table(rows=6, cols=6)
table3.style = 'Table Grid'
table3.alignment = WD_TABLE_ALIGNMENT.CENTER

headers3 = ['T(k,0)', 'T(k,1)', 'T(k,2)', 'T(k,3)', 'T(k,4)', 'T(k,5)']
rom_data = [
    ['0.7853981634', '---', '---', '---', '---', '---'],
    ['0.9480594490', '1.0022798775', '---', '---', '---', '---'],
    ['0.9871158010', '1.0001345850', '0.9999915655', '---', '---', '---'],
    ['0.9967851719', '1.0000082955', '0.9999998762', '1.0000000081', '---', '---'],
    ['0.9991966805', '1.0000005167', '0.9999999981', '1.0000000000', '0.999999999998', '---'],
]

for j, header in enumerate(headers3):
    cell = table3.rows[0].cells[j]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(9)
            run.font.name = '宋体'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

for i, row_data in enumerate(rom_data):
    for j, val in enumerate(row_data):
        cell = table3.rows[i+1].cells[j]
        cell.text = val
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(9)
                run.font.name = 'Courier New'

doc.add_paragraph()

p = doc.add_paragraph('表4  Gauss-Legendre不同节点数的精度对比')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.bold = True
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 表4 - GL不同节点
table4 = doc.add_table(rows=6, cols=3)
table4.style = 'Table Grid'
table4.alignment = WD_TABLE_ALIGNMENT.CENTER

headers4 = ['节点数 n', '近似值', '绝对误差']
gl_data = [
    ['1', '1.110720734539592', '1.11×10⁻¹'],
    ['2', '0.998472613404115', '1.53×10⁻³'],
    ['3', '1.000008121555496', '8.12×10⁻⁶'],
    ['4', '0.999999977197110', '2.28×10⁻⁸'],
    ['5', '1.000000000039559', '3.96×10⁻¹¹'],
]

for j, header in enumerate(headers4):
    cell = table4.rows[0].cells[j]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)
            run.font.name = '宋体'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

for i, row_data in enumerate(gl_data):
    for j, val in enumerate(row_data):
        cell = table4.rows[i+1].cells[j]
        cell.text = val
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(10)
                run.font.name = '宋体'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_paragraph()

# 插入图片
p = doc.add_paragraph('图1  各数值积分方法误差收敛曲线')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.bold = True
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

fig1_path = os.path.join(base_dir, 'fig1_convergence.png')
if os.path.exists(fig1_path):
    doc.add_picture(fig1_path, width=Inches(6.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()

p = doc.add_paragraph('图2  被积函数f(x) = cos(x)在[0, π/2]上的图像与积分区域')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.bold = True
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

fig2_path = os.path.join(base_dir, 'fig2_integrand.png')
if os.path.exists(fig2_path):
    doc.add_picture(fig2_path, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# 结果分析
h2 = doc.add_heading('2. 结果分析与讨论思考', level=2)
for run in h2.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

h3 = doc.add_heading('（1）计算结果分析与比较方法的优缺点及其适用场景', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

analysis1 = [
    '① 算法正确性验证：',
    '表2显示所有四种方法对∫₀¹ x² dx的计算均达到或接近机器精度（10⁻¹⁵量级），验证了各算法程序的正确性。其中自适应Simpson和Romberg均精确到10⁻¹⁵以上，Gauss-Legendre仅需5个节点即达此精度。',
    '',
    '② 精度对比（以目标积分为基准）：',
    '• Romberg求积精度最高（误差~10⁻¹²），仅需4次迭代即达到极高精度。Richardson外推逐次消去截断误差低阶项，使T表对角线元素极速收敛。',
    '• 自适应Simpson求积精度良好（误差~10⁻¹⁰），仅需3层递归。Simpson公式本身的4阶收敛配合自适应策略，有效减少了函数值计算。',
    '• Gauss-Legendre求积精度极高（n=5时误差~10⁻¹¹），5个节点即几乎达到机器精度。cos(x)为光滑函数，Gauss公式2n+1次代数精度的优势充分发挥。',
    '• 变步长梯形求积精度最低（误差~10⁻⁸），需11次迭代（2049节点）。梯形公式O(h²)收敛速度在此仍满足ε = 0.5×10⁻⁶的要求，但效率最低。',
    '',
    '③ 收敛速度分析（结合表3和图1）：',
    '• 变步长梯形：一阶收敛O(h²)，收敛曲线在对数坐标中呈线性下降，斜率约-2。',
    '• 自适应Simpson：高阶收敛O(h⁴)，收敛曲线斜率约-4，约为梯形的2倍。',
    '• Romberg：超线性收敛。从T表可清楚看到：梯形列从0.785→1.000需4次迭代，Simpson列仅需3次，Cotes列仅需2次，Romberg对角线在第4次迭代已收敛到精确值。',
    '• Gauss-Legendre收敛：指数型收敛趋势。n=2时误差~10⁻³，n=3时降至~10⁻⁶，n=4时降至~10⁻⁸，n=5时降至~10⁻¹¹。',
    '',
    '④ 计算效率分析：',
    '• 函数值计算次数：Gauss-Legendre(5次) < Romberg(31次) < 自适应Simpson(~40次) << 变步长梯形(2049次)',
    '• 算法复杂度：变步长梯形最简单（循环），Romberg次之（循环+外推），Gauss-Legendre需预存节点表计算，自适应Simpson需栈管理递归。',
]
for text in analysis1:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 方法优缺点对比表
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('表5  四种数值积分方法综合对比')
run.bold = True
run.font.name = '宋体'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

table5 = doc.add_table(rows=5, cols=5)
table5.style = 'Table Grid'
table5.alignment = WD_TABLE_ALIGNMENT.CENTER

headers5 = ['方法', '优点', '缺点', '收敛阶', '适用场景']
data5 = [
    ['变步长梯形', '算法简单，函数值可复用，具有后验误差估计', '收敛速度慢O(h²)，代数精度低', 'O(h²)', '精度要求不高或作为Romberg初始序列'],
    ['自适应Simpson', '自适应区间划分，对非均匀光滑函数适应性好', '递归实现复杂，函数值复用性差', 'O(h⁴)', '函数光滑性不均匀的中等精度场景'],
    ['Romberg', '收敛速度快，精度极高，数值稳定性好', '要求函数充分光滑，实现稍复杂', '超线性', '光滑函数高精度积分的首选'],
    ['Gauss-Legendre', '代数精度最高，函数求值次数最少，谱精度', '节点不规则，函数值不能复用', '指数型', '光滑函数高精度，函数求值代价高'],
]

for j, header in enumerate(headers5):
    cell = table5.rows[0].cells[j]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(9)
            run.font.name = '宋体'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

for i, row_data in enumerate(data5):
    for j, val in enumerate(row_data):
        cell = table5.rows[i+1].cells[j]
        cell.text = val
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(9)
                run.font.name = '宋体'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_paragraph()

h3 = doc.add_heading('（2）上机实验中遇到问题及其解决方案', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

problems = [
    '问题1：Gauss-Legendre求积初始实现中Newton-Raphson迭代收敛到重复节点，导致结果错误。',
    '解决方案：改用对称性策略——仅计算正半轴上的m = ⌈(n+1)/2⌉个节点，再通过x→-x对称性获得全部节点。同时改进初始猜测公式为cos(π(4i-3)/(4n+2))，提高收敛稳定性。',
    '',
    '问题2：自适应Simpson递归实现在MATLAB中出现栈溢出或无限递归。',
    '解决方案：改用基于栈的迭代实现。使用显式栈数据结构替代隐式递归调用，避免了MATLAB递归深度限制问题，同时保持了自适应细分的核心逻辑。',
    '',
    '问题3：变步长梯形求积收敛缓慢，需要较多节点（2049个）才能达到0.5×10⁻⁶精度。',
    '解决方案：在精度要求较高的场景中改用Romberg方法。Romberg方法正是利用变步长梯形序列作为基础，通过Richardson外推大幅提高收敛速度。变步长梯形可作为Romberg的初始化步骤。',
]
for text in problems:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

h3 = doc.add_heading('（3）算法改进及其建议', level=3)
for run in h3.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

improvements = [
    '① 自适应Romberg：将自适应区间细分思想与Romberg外推结合——先自适应划分区间，再在每个子区间上使用Romberg外推，适应函数局部光滑性差异。',
    '② 自适应Gauss求积：将自适应Simpson中的区间细分思想推广至Gauss求积，在每个子区间上使用2点或3点Gauss-Legendre公式代替Simpson公式。',
    '③ 混合策略：先用自适应方法划分区间，在每个子区间上根据函数光滑性选择最优方法——光滑区用Romberg或Gauss，非光滑区用低阶复合求积。',
    '④ 并行化：复合求积中各子区间的函数值计算相互独立，适合GPU并行加速，对大批量积分计算可显著提速。',
    '⑤ 其他Gauss型求积拓展：对于振荡函数可用Gauss-Chebyshev；半无穷区间[0,+∞)用Gauss-Laguerre；全无穷区间(-∞,+∞)用Gauss-Hermite。',
]
for text in improvements:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_page_break()

# ==================== 实验结论 ====================
h = doc.add_heading('实验结论', level=1)
for run in h.runs:
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

conclusions = [
    '1. 通过本次实验，成功实现了变步长梯形求积、自适应Simpson求积、Romberg求积与Gauss-Legendre求积的算法编程，并在MATLAB中验证了程序的正确性。',
    '2. 对于目标积分∫₀^{π/2} cos(x) dx = 1，四种方法均在ε = 0.5×10⁻⁶的精度要求下给出了满意的结果：Romberg精度最高（误差~10⁻¹²），Gauss-Legendre次之（误差~10⁻¹¹），自适应Simpson（误差~10⁻¹⁰），变步长梯形（误差~10⁻⁸）。',
    '3. 通过Romberg T表的详细分析，直观展示了Richardson外推逐次消去截断误差低阶项的加速效果——梯形列需4次迭代才能接近精确值，而Romberg对角线在第4次迭代即达到10⁻¹²精度。',
    '4. Gauss-Legendre求积展现了"以最少节点获最高精度"的优越性——仅需5个节点即达到10⁻¹¹精度，适合被积函数计算代价高昂的场合。',
    '5. 比较了不同方法的性能特点，加深了对变步长求积、Richardson外推和最优求积节点选择等数值积分核心概念的理解。',
]
for text in conclusions:
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = '宋体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

doc.add_paragraph()
doc.add_paragraph()

# 保存
output_path = os.path.join(base_dir, '李圣元2024150118实验十四_完成.docx')
doc.save(output_path)
print(f'Report saved to: {output_path}')
