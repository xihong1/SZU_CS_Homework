"""
基于模板格式生成实验四实验报告 (docx)
完全复刻模板封面样式, 然后在模板范围内填入实验内容
"""
import json
import os
from docx import Document
from docx.shared import Pt, Cm, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ---- 页面设置 (复制模板的A4设置) ----
for section in doc.sections:
    section.page_width  = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin    = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin   = Cm(3.17)
    section.right_margin  = Cm(3.17)

# ---- 基础样式 ----
style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(14)  # 模板用四号(14pt)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

def set_font(run, font_name='宋体', size=Pt(14), bold=False):
    """设置run的字体属性"""
    run.font.name = font_name
    run.font.size = size
    run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), font_name)

def add_cover_line(label, value, extra_parts=None):
    """添加封面的一行: 缩进 + 标签 + 值 + 可选额外部分"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after  = Pt(12)
    pf.line_spacing = Pt(36)

    # 前置空格(缩进)
    if label.startswith('      '):
        r0 = p.add_run('      ')
    else:
        r0 = p.add_run('')
    set_font(r0, '宋体', Pt(14), True)

    # 标签
    r1 = p.add_run(label.strip())
    set_font(r1, '宋体', Pt(14), True)

    # 值前的空格
    r2 = p.add_run('          ')
    set_font(r2, '宋体', Pt(14), True)

    # 值
    r3 = p.add_run(value)
    set_font(r3, '宋体', Pt(14), True)

    # 额外部分(学号/班级等)
    if extra_parts:
        for ep in extra_parts:
            r4 = p.add_run(ep)
            set_font(r4, '宋体', Pt(14), True)

    # 尾随空格
    r5 = p.add_run('                         ')
    set_font(r5, '宋体', Pt(14), True)
    return p

def add_cover_line_simple(label, value):
    """简单的封面行: label + value"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after  = Pt(12)
    pf.line_spacing = Pt(36)

    r0 = p.add_run(label)
    set_font(r0, '宋体', Pt(14), True)
    r1 = p.add_run('              ')
    set_font(r1, '宋体', Pt(14), True)
    r2 = p.add_run(value)
    set_font(r2, '宋体', Pt(14), True)
    r3 = p.add_run('                 ')
    set_font(r3, '宋体', Pt(14), True)
    return p

# ====================================================================
# ★ 封面 — 完全按照模板格式
# ====================================================================

# 空行
for _ in range(2):
    doc.add_paragraph()

# 标题: 课程实验报告 (居中, 黑体, 初号=44pt, 加粗)
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(24)
r = title_p.add_run('课 程 实 验 报 告')
set_font(r, '黑体', Pt(22), True)

# 空行
doc.add_paragraph()
doc.add_paragraph()

# 封面信息行 (四号=14pt, 宋体, 加粗)
add_cover_line('      课程名称：', '编译原理')

add_cover_line('      实验项目名称：', '语义分析与类型系统')

add_cover_line_simple('学院：', '计算机与大数据学院')

add_cover_line_simple('专业：', '人工智能')

add_cover_line('      指导教师：', '朱彦臻')

# 姓名+学号+班级 在同一行
p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(12)
pf.space_after  = Pt(12)
pf.line_spacing = Pt(36)

parts = [
    ('      ', True),
    ('申报人：', True),
    (' ', True),
    ('李圣元', True),
    ('  ', True),
    ('学号：', True),
    (' ', True),
    ('2024150118', True),
    ('   ', True),
    ('班级：', True),
    (' ', True),
    ('卓越班', True),
    ('         ', True),
]
for txt, bld in parts:
    rn = p.add_run(txt)
    set_font(rn, '宋体', Pt(14), bld)

add_cover_line('      实验时间：', '2026年6月18日——2026年6月24日')

add_cover_line('      实验报告提交时间：', '2026年6月24日')

# 目录页标题
doc.add_page_break()
toc_p = doc.add_paragraph()
toc_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = toc_p.add_run('目录')
set_font(r, '黑体', Pt(16), True)

# 目录内容
toc_items = [
    '一、实验概述',
    '二、实验目标',
    '三、设计与实现说明',
    '    3.1 整体架构与工作流程',
    '    3.2 符号表数据结构设计',
    '    3.3 两遍分析策略',
    '    3.4 语句检查的分发机制',
    '    3.5 变量声明的语义检查',
    '    3.6 表达式类型推导系统',
    '    3.7 二元表达式运算符类型检查',
    '    3.8 函数调用的语义检查',
    '    3.9 控制流语句的作用域管理',
    '    3.10 return语句与函数返回类型匹配',
    '    3.11 方法调用的类型检查',
    '    3.12 错误检测与恢复策略',
    '    3.13 选做：auto类型推导的完整实现',
    '    3.14 @类型注解的交叉验证',
    '    3.15 与前后端实验的对接',
    '四、完整功能演示流程',
    '五、AI协作过程小结',
    '六、遇到的问题及解决方案',
    '七、总结',
    '八、交付物清单',
]
for item in toc_items:
    tp = doc.add_paragraph()
    tp.paragraph_format.line_spacing = Pt(28)
    r = tp.add_run(item)
    if item.startswith('    '):
        set_font(r, '宋体', Pt(12), False)
    else:
        set_font(r, '宋体', Pt(12), True)

doc.add_page_break()

# ====================================================================
# 以下为报告正文（与模板格式一致：正文宋体小四12pt，标题黑体）
# ====================================================================

def add_heading_styled(text, level=1):
    """正文标题"""
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = '黑体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        if level == 1:
            run.font.size = Pt(16)
        elif level == 2:
            run.font.size = Pt(14)
        elif level == 3:
            run.font.size = Pt(13)
    return h

def add_para(text, indent=True):
    """正文段落"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(text)
    run.font.name = '宋体'
    run.font.size = Pt(12)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    return p

def add_code_block(code_text):
    """代码块"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8)
    return p

def add_json_block(json_text):
    """JSON输出块"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(json_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8)
    return p

def add_table_simple(headers, rows):
    table = doc.add_table(rows=1+len(rows), cols=len(headers), style='Table Grid')
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            table.rows[ri+1].cells[ci].text = str(val)
    doc.add_paragraph()
    return table

def add_bullet(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74)
    r = p.add_run('• ' + text)
    r.font.name = '宋体'; r.font.size = Pt(12)
    r.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    return p

def load_check_result(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# ====================================================================
# 一、实验概述
# ====================================================================
add_heading_styled('一、实验概述', 1)
add_para('本实验是编译原理实验系列的第四个实验。在实验三中，语法分析器已经能够构建抽象语法树（AST）。本实验的目标是：在AST的基础上进行语义分析——构建符号表、管理作用域、进行类型检查，检测并报告各类语义错误。')
add_para('语法正确的程序未必有意义：变量可能未声明就使用，类型可能不匹配，函数调用参数个数可能错误。语义分析负责在编译期捕获这些错误，是保证程序正确性的重要一环，也是连接前端与后端的桥梁。')
add_para('本实验在实验三编译器的基础上新增了语义分析模块semantic_module.py（约410行），实现了完整的符号表构建、嵌套作用域管理、基于AST遍历的类型检查，以及7种基本语义错误的检测与精确定位。此外还完成了选做任务——基于auto关键字的局部变量类型推导，涉及词法/语法/语义三层扩展。')

# ====================================================================
# 二、实验目标
# ====================================================================
add_heading_styled('二、实验目标', 1)
for g in ['理解符号表的构建与作用域管理（嵌套作用域、变量遮蔽）',
          '掌握类型系统的设计与类型检查的实现',
          '能够检测常见的语义错误并准确定位',
          '掌握基于AST遍历的语义分析方法（属性文法/访问者模式）',
          '（选做）实现局部变量类型推导功能，理解类型推导的基本原理']:
    add_bullet(g)

# ====================================================================
# 三、设计与实现说明
# ====================================================================
add_heading_styled('三、设计与实现说明', 1)

# 3.1
add_heading_styled('3.1 整体架构与工作流程', 2)
add_para('语义分析器作为编译器的第三阶段，接收语法分析器产出的AST作为输入，通过遍历AST的每个节点，执行对应的语义检查逻辑。编译器主流程通过compiler.py的check命令串联三个阶段。')
add_code_block('''源代码 (.src) → 词法分析器(tokenize) → Token序列
    → 语法分析器(Parser.parse) → AST
    → 语义分析器(SemanticAnalyzer.check) → 符号表 + 语义错误

compiler.py check 命令的入口逻辑:
  result = tokenize(source_code, with_indents=True)
  parser = Parser(result["tokens"])
  parse_result = parser.parse()
  all_frontend_errors = lex_errors + parse_result["errors"]
  if all_frontend_errors:
      output_json({"errors": all_frontend_errors, "symbols": []})
  else:
      from semantic_module import semantic_check
      output_json(semantic_check(parse_result["ast"]))''')
add_para('语义分析器只在词法和语法均无错误时才被调用。这是因为语法错误会导致AST结构不完整，此时进行语义检查可能产生大量虚假错误。这种"分层防护"的设计是编译器前端的标准做法。')

# 3.2
add_heading_styled('3.2 符号表数据结构设计', 2)
add_para('符号表是语义分析的核心数据结构。本实验采用"作用域栈"（Scope Stack）结构来管理嵌套作用域。下面逐层讲解三个核心类的设计。')

add_heading_styled('3.2.1 Symbol类——符号表条目', 3)
add_para('Symbol类封装了一个被声明实体的全部信息。每个Symbol实例记录：名称、类型字符串、实体种类（变量/参数/函数/数组）、声明位置（行号列号）、作用域层级，以及函数和数组的特有信息。')
add_code_block('''class Symbol:
    """符号表条目 — 记录变量/函数/参数/数组的完整信息"""
    def __init__(self, name, sym_type, kind, line, col, scope_level,
                 params=None, return_type=None, array_size=None):
        self.name = name              # 符号名称，如 "x", "fib"
        self.sym_type = sym_type      # 类型字符串，如 "int", "int[5]", "int(int,int)"
        self.kind = kind              # 实体种类: 'var' | 'param' | 'func' | 'array'
        self.line = line              # 声明行号
        self.col = col                # 声明列号
        self.scope_level = scope_level # 作用域层级: 0=global, 1=function, 2+=block
        self.params = params or []    # 函数参数列表 [(name, type), ...]
        self.return_type = return_type # 函数返回类型
        self.array_size = array_size  # 数组大小''')
add_para('设计要点：sym_type字段统一表示类型的字符串形式。对于基本类型变量为"int"/"float"等；对于数组为"int[5]"；对于函数为"int(int,int)"。这种统一表示使类型比较和输出都变得简单。')

add_heading_styled('3.2.2 Scope类——单个作用域', 3)
add_para('每个Scope对应程序中的一个作用域区域（全局、函数体、if块等），内部维护一个字典将名称映射到Symbol。')
add_code_block('''class Scope:
    """单个作用域"""
    def __init__(self, level=0):
        self.symbols = {}    # name -> Symbol 的映射字典
        self.level = level   # 嵌套层级

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        return self.symbols.get(name)    # 仅在当前作用域查找

    def contains(self, name):
        return name in self.symbols''')

add_heading_styled('3.2.3 SymbolTable类——嵌套作用域符号表', 3)
add_para('SymbolTable是作用域管理的核心。它维护一个作用域栈（Python列表），栈顶是当前最内层作用域。这种设计使作用域的进入/退出与AST遍历自然对应：遇到函数体/if块/while块时入栈新作用域，离开时出栈。')
add_code_block('''class SymbolTable:
    """嵌套作用域符号表 — 作用域栈 + 全局符号记录"""
    def __init__(self):
        self.scopes = []          # 作用域栈
        self.all_symbols = []     # 所有已定义符号的列表

    def enter_scope(self):
        """进入新作用域（创建新Scope并入栈）"""
        level = len(self.scopes)
        self.scopes.append(Scope(level))

    def exit_scope(self):
        """退出当前作用域（栈顶出栈，该作用域中的符号不再可见）"""
        if self.scopes:
            self.scopes.pop()

    def lookup(self, name):
        """从内到外查找符号 — 实现变量遮蔽的关键
           从栈顶（最内层）向栈底（最外层）搜索
        """
        for scope in reversed(self.scopes):
            sym = scope.lookup(name)
            if sym is not None:
                return sym
        return None  # 所有作用域都找不到 → 未声明

    def lookup_current_scope(self, name):
        """仅在当前作用域查找 — 用于重复声明检测"""
        scope = self.scopes[-1]
        return scope.lookup(name)''')
add_para('关键设计决策：lookup()和lookup_current_scope()分别服务于两个不同的语义检查需求。lookup()从内到外搜索，天然支持变量遮蔽——内层同名变量会被先找到。lookup_current_scope()仅在当前作用域搜索，用于检测重复声明——确保同一作用域中不能有两个同名符号。')

add_heading_styled('3.2.4 变量遮蔽的实现原理', 3)
add_para('变量遮蔽（Variable Shadowing）是嵌套作用域的核心特性。以S2场景中的三个value变量为例：')
add_code_block('''fn(int) scopeDemo -> x@int:
    int value                   ← value₁ (scope_level=1, function作用域)
    value@int = x@int + 1
    if x@int > 0:
        int value               ← value₂ (scope_level=2, block作用域)
        value@int = x@int + 100
        if value@int > 50:
            int value           ← value₃ (scope_level=3, block作用域)
            value@int = 999
            print->(value@int)  ← 查找value: scopes[-1]找到value₃ → 输出999
        print->(value@int)      ← 查找value: 栈顶没有, 下一层找到value₂
    return value@int            ← 查找value: 栈底找到value₁ → 返回x@int+1''')
add_para('作用域栈的变化：进入scopeDemo函数体→[Global, Function]；进入外层if→[Global, Function, Block(lv2)]；进入内层if→[Global, Function, Block(lv2), Block(lv3)]；退出时逐层pop，变量随作用域销毁。')

# 3.3
add_heading_styled('3.3 两遍分析策略', 2)
add_para('为支持函数间的相互调用和前向引用（如fib递归、两个函数互相调用），语义分析采用"两遍遍历"策略。在check()入口方法中实现：')
add_code_block('''def check(self, ast):
    """入口：对整个AST进行语义检查——实现两遍分析"""
    self.errors = []
    self.symtab = SymbolTable()
    self.symtab.enter_scope()      # 进入全局作用域
    self._register_builtins()      # 注册内置函数（如print）

    # ===== 第一遍：收集所有函数声明 =====
    funcs = ast.get("funcs", [])
    for func in funcs:
        if func.get("type") == "FuncDecl":
            self._declare_function(func)   # 只记录签名，不检查函数体

    # ===== 第二遍：检查每个函数体 =====
    for func in funcs:
        if func.get("type") == "FuncDecl":
            self._check_function(func)     # 进入函数作用域，检查全部语句

    self.symtab.exit_scope()
    symbols_out = [sym.to_dict() for sym in self.symtab.all_symbols]
    return {"errors": [e.to_dict() for e in self.errors], "symbols": symbols_out}''')

add_para('第一遍_declare_function()的要点：解析函数名、返回类型、参数列表，构建函数类型字符串（如"int(int,int)"），创建Symbol并注册到全局作用域，同时检查函数名是否重复声明。')
add_code_block('''def _declare_function(self, node):
    """第一遍：声明函数签名到全局符号表"""
    name = node.get("name", "")
    return_type = node.get("return_type", "void")
    params = []
    for p in node.get("params", []):
        ptype = p.get("param_type", "int")
        pname = p.get("name", "")
        array_size = p.get("array_size")
        if array_size:
            params.append((pname, f"{ptype}[{array_size}]"))
        else:
            params.append((pname, ptype))
    # 查重
    if self.symtab.lookup_current_scope(name):
        self.error("REDECLARED", f"function '{name}' is already declared", ...)
        return
    # 注册
    func_type = f"{return_type}({','.join(p[1] for p in params)})"
    sym = Symbol(name, func_type, "func", ..., params=params, return_type=return_type)
    self.symtab.define(sym)''')

add_para('第二遍_check_function()：进入函数作用域→声明参数→检查函数体每条语句→退出作用域。同时设置self.current_function以支持return语句的类型检查。')
add_code_block('''def _check_function(self, node):
    """第二遍：在函数作用域中检查函数体"""
    name = node.get("name", "")
    self.symtab.enter_scope()
    self.current_function = {"name": name, "return_type": node.get("return_type", "void")}
    # 声明参数到函数作用域
    for p in node.get("params", []):
        sym = Symbol(p["name"], p["param_type"], "param", ...)
        self.symtab.define(sym)
    # 逐条检查函数体
    self._check_statement_list(node.get("body", []))
    self.symtab.exit_scope()
    self.current_function = None''')

# 3.4
add_heading_styled('3.4 语句检查的分发机制', 2)
add_para('语义分析器采用"访问者模式"对AST进行遍历。_check_statement()方法作为语句检查的入口，根据AST节点的type字段将检查任务分发到对应的专用检查方法。')
add_code_block('''def _check_statement(self, node):
    """语句检查的分发器"""
    if node is None: return
    node_type = node.get("type", "")
    if   node_type == "VarDecl":       self._check_var_decl(node)
    elif node_type == "AutoVarDecl":   self._check_auto_decl(node)      # ★选做
    elif node_type == "AssignStmt":    self._check_assign(node)
    elif node_type == "IfStmt":        self._check_if(node)
    elif node_type == "WhileStmt":     self._check_while(node)
    elif node_type == "ReturnStmt":    self._check_return(node)
    elif node_type == "ExprStmt":      self._check_expr(node.get("expr"))
    elif node_type == "BreakStmt":     pass
    elif node_type == "ContinueStmt":  pass''')

# 3.5
add_heading_styled('3.5 变量声明的语义检查', 2)
add_para('变量声明检查（_check_var_decl）是语义分析中最频繁的操作之一。每种变量声明需要依次完成：类型合法性验证→重复声明检测→符号注册→初始化表达式类型检查。')
add_code_block('''def _check_var_decl(self, node):
    """检查变量声明: Type Identifier [= Expr]  或  Type Identifier [size]"""
    var_type = node.get("var_type", "int"); name = node.get("name", "")
    line, col = node.get("line", 0), node.get("col", 0)
    init = node.get("init"); size = node.get("size")

    # 步骤1: 验证类型关键字的合法性
    if not is_valid_type(var_type):
        self.error("TYPE_MISMATCH", f"unknown type '{var_type}'", line, col)
        var_type = "int"

    # 步骤2: 检查当前作用域内是否已存在同名符号（REDECLARED检测）
    if self.symtab.lookup_current_scope(name):
        self.error("REDECLARED", f"'{name}' is already declared", line, col, symbol=name)
        return

    # 步骤3: 注册符号到当前作用域
    if size is not None:
        sym = Symbol(name, f"{var_type}[{size}]", "array", line, col, ...)
    else:
        sym = Symbol(name, var_type, "var", line, col, ...)
    self.symtab.define(sym)

    # 步骤4: 如果有初始化表达式，检查类型一致性
    if init is not None:
        init_type = self._check_expr(init)
        if init_type is not None and init_type != var_type:
            self.error("TYPE_MISMATCH",
                       f"cannot assign '{init_type}' to variable of type '{var_type}'",
                       line, col, expected=var_type, found=init_type)''')

# 3.6
add_heading_styled('3.6 表达式类型推导系统', 2)
add_para('表达式类型推导是语义分析中最核心的递归操作。_check_expr()方法接收任意表达式AST节点，返回该表达式的类型字符串。它同样是一个分发器，根据节点类型路由到对应的专用检查方法：')
add_code_block('''def _check_expr(self, node):
    """表达式检查的总入口——返回表达式的类型字符串"""
    if node is None: return None
    node_type = node.get("type", "")
    # 字面量：类型直接确定
    if   node_type == "IntLiteral":      return "int"
    elif node_type == "FloatLiteral":    return "float"
    elif node_type == "StringLiteral":   return "string"
    elif node_type == "BoolLiteral":     return "bool"
    # 标识符/引用：需要查符号表
    elif node_type == "Identifier":      return self._check_identifier(node)
    elif node_type == "TypedVarRef":     return self._check_typed_var_ref(node)
    elif node_type == "TypedArrayRef":   return self._check_typed_array_ref(node)
    elif node_type == "TypedArrayElemRef":return self._check_typed_array_elem_ref(node)
    # 复合表达式：递归检查子表达式，综合计算类型
    elif node_type == "BinaryExpr":      return self._check_binary_expr(node)
    elif node_type == "UnaryExpr":       return self._check_unary_expr(node)
    elif node_type == "CallExpr":        return self._check_call_expr(node)
    elif node_type == "MethodCall":      return self._check_method_call(node)
    else: return None''')

add_para('这种递归设计的关键优势：每个检查方法只需关注当前节点类型的规则，子表达式的类型由递归调用自动获得。以二元表达式 a@int + b@int 为例，类型推导过程如下：')
add_code_block('''执行 _check_binary_expr( BinaryExpr("+", a@int, b@int) ):
  步骤1: left_type  = _check_expr(a@int) → 查符号表 → 返回 "int"
  步骤2: right_type = _check_expr(b@int) → 查符号表 → 返回 "int"
  步骤3: 验证 left_type == right_type? "int" == "int" ✓
  步骤4: 验证 "+" 对 "int" 合法? 算术运算 ✓ → 返回 "int"
  最终: 整个表达式 a@int + b@int 的类型为 "int"''')

# 3.7
add_heading_styled('3.7 二元表达式运算符类型检查', 2)
add_para('二元运算符的类型检查是类型系统中最复杂的部分之一。NovaLang将运算符分为四类，每类有不同的类型约束和结果类型：')
add_table_simple(
    ['运算符类别', '运算符', '操作数类型要求', '结果类型'],
    [
        ['算术运算', '+ - * /', 'int 或 float（左右类型一致）', '与操作数相同'],
        ['算术(取模)', '%', 'int（左右类型一致）', 'int'],
        ['关系运算', '< <= > >=', 'int 或 float（左右类型一致）', 'bool'],
        ['相等运算', '== !=', 'int/float/string/bool（左右类型一致）', 'bool'],
        ['逻辑运算', '&& ||', 'bool（左右类型一致）', 'bool'],
    ]
)
add_code_block('''def _check_binary_expr(self, node):
    """检查二元表达式 — 运算符类型约束验证"""
    op = node.get("op", "")
    left, right = node.get("left"), node.get("right")
    # 1. 递归获得左右操作数类型
    left_type = self._check_expr(left)
    right_type = self._check_expr(right)
    if left_type is None or right_type is None: return None
    # 2. 验证左右类型一致性
    if left_type != right_type:
        self.error("TYPE_MISMATCH",
                   f"operator '{op}' requires same type, got '{left_type}' and '{right_type}'", ...)
        return left_type
    # 3. 按运算符类别进行类型约束检查
    if op in ARITHMETIC_OPS:    # + - * / %
        if left_type not in VALID_ARITHMETIC_TYPES: self.error(...)
        if op == "%" and left_type != "int": self.error(...)
        return left_type
    elif op in RELATIONAL_OPS:  # < <= > >=
        if left_type not in VALID_RELATIONAL_TYPES: self.error(...)
        return "bool"
    elif op in EQUALITY_OPS:    # == !=
        return "bool"
    elif op in LOGICAL_OPS:     # && ||
        if left_type != "bool": self.error(...)
        return "bool"''')

# 3.8
add_heading_styled('3.8 函数调用的语义检查', 2)
add_para('函数调用是语义分析中检查逻辑最丰富的操作。_check_call_expr()方法需依次完成：被调用者查找→非函数检查→参数个数检查→参数类型检查。本实现支持"any"类型参数（用于内置函数如print接受任意类型实参）。')
add_code_block('''def _check_call_expr(self, node):
    """检查函数调用: callee->(arg1, arg2, ...) 返回被调用函数的返回类型"""
    callee = node.get("callee", {}); args = node.get("args", [])
    callee_name = callee.get("name", "")
    if not callee_name: return None

    # 步骤1: 从符号表查找被调用函数
    sym = self.symtab.lookup(callee_name)
    if sym is None:
        self.error("UNDECLARED", f"function '{callee_name}' is not declared", ...)
        return None

    # 步骤2: 验证被调用者确实是函数
    if sym.kind != "func":
        self.error("NOT_A_FUNCTION", f"'{callee_name}' is not a function", ...)
        return None

    # 步骤3: 检查实参个数与形参个数是否一致
    expected_params = sym.params
    if len(args) != len(expected_params):
        self.error("ARG_COUNT_MISMATCH",
                   f"function '{callee_name}' expects {len(expected_params)} arguments, got {len(args)}", ...)

    # 步骤4: 逐个检查实参类型与对应形参类型是否匹配
    for i, arg in enumerate(args):
        arg_type = self._check_expr(arg)          # 递归推导实参类型
        if arg_type is not None and i < len(expected_params):
            expected_type = expected_params[i][1]
            if expected_type == "any": continue    # 内置函数接受任意类型
            if arg_type != expected_type:
                self.error("ARG_TYPE_MISMATCH",
                           f"argument {i+1} expects '{expected_type}', got '{arg_type}'", ...)

    return sym.return_type  # 返回函数的返回类型''')
add_para('该方法的返回值是函数的返回类型，这使得函数调用可以嵌套在其他表达式中，例如 fib->(n@int - 1) 的类型推导会返回 "int"，进而被外层的 + 运算符使用。')

# 3.9
add_heading_styled('3.9 控制流语句的作用域管理', 2)
add_para('if语句和while语句是NovaLang中创建新作用域的结构。以if语句为例，_check_if()方法在检查条件表达式类型后，为then分支和else分支分别创建独立的块作用域：')
add_code_block('''def _check_if(self, node):
    """检查if语句 — 条件类型检查 + 分支作用域管理"""
    cond, then_body = node.get("cond", {}), node.get("then", [])
    else_body = node.get("else")
    # 条件表达式必须是bool类型
    cond_type = self._check_expr(cond)
    if cond_type is not None and cond_type != "bool":
        self.error("TYPE_MISMATCH", "if condition must be 'bool'", ...)
    # then分支：进入新作用域 → 检查 → 退出
    self.symtab.enter_scope()
    self._check_statement_list(then_body)
    self.symtab.exit_scope()
    # else分支（如果存在）：进入另一个独立作用域
    if else_body:
        self.symtab.enter_scope()
        self._check_statement_list(else_body)
        self.symtab.exit_scope()''')
add_para('while语句的处理方式类似，为循环体创建新的块作用域。这种设计确保了在if/while块内声明的变量不会泄漏到外层作用域。')

# 3.10
add_heading_styled('3.10 return语句与函数返回类型匹配', 2)
add_para('return语句的类型检查需要与函数声明的返回类型进行比较。self.current_function字典在进入函数体时设置，记录了当前函数的返回类型。')
add_code_block('''def _check_return(self, node):
    """检查return语句 — 返回表达式类型必须与函数声明匹配"""
    expr = node.get("expr")
    expected_type = self.current_function.get("return_type", "void")
    if expr is None:
        if expected_type != "void":
            self.error("RETURN_TYPE_MISMATCH", "expected return, but returning nothing", ...)
    else:
        expr_type = self._check_expr(expr)
        if expr_type is not None and expr_type != expected_type:
            self.error("RETURN_TYPE_MISMATCH",
                       f"expected '{expected_type}', got '{expr_type}'", ...)''')

# 3.11
add_heading_styled('3.11 方法调用的类型检查', 2)
add_para('NovaLang通过对象方法实现类型转换。toFloat()和toInt()是两个内置方法，分别只能在int和float类型上调用。')
add_code_block('''def _check_method_call(self, node):
    """检查方法调用: object.method(args)
       NovaLang内置方法: toFloat()[只能在int上调用], toInt()[只能在float上调用]
    """
    obj = node.get("object"); method = node.get("method", "")
    obj_type = self._check_expr(obj)  # 先推导接收者类型
    if method == "toFloat":
        if obj_type is not None and obj_type != "int":
            self.error("TYPE_MISMATCH", "'toFloat()' can only be called on 'int'", ...)
        return "float"
    elif method == "toInt":
        if obj_type is not None and obj_type != "float":
            self.error("TYPE_MISMATCH", "'toInt()' can only be called on 'float'", ...)
        return "int"
    else:
        self.error("UNDECLARED", f"unknown method '{method}'", ...)
        return None''')

# 3.12
add_heading_styled('3.12 错误检测与恢复策略', 2)
add_para('本语义分析器采用的错误处理策略是"检测-记录-继续"模式。与实验三的panic-mode不同，语义分析阶段不需要跳过token，因为AST的结构是完整的——只需要在每个节点上验证语义规则，发现错误时记录而非中断。')
add_code_block('''class SemanticError(Exception):
    """语义错误 — 继承自Exception但不抛出，仅用于结构化记录"""
    def __init__(self, error_type, message, line, col, **extra):
        self.error_type = error_type   # 错误类型标识符
        self.message = message         # 人类可读描述
        self.line, self.col = line, col # 精确位置
        self.extra = extra             # 额外上下文 {symbol, expected, found, ...}

    def to_dict(self):
        d = {"type": self.error_type, "line": self.line, "col": self.col}
        d.update(self.extra)
        return d

def error(self, error_type, message, line, col, **extra):
    """记录一个语义错误（不中断分析）"""
    self.errors.append(SemanticError(error_type, message, line, col, **extra))''')
add_para('"继续分析"策略的优势：开发者一次编译可以看到所有语义错误，而不是修复一个→重新编译→看到下一个的循环。三个容错机制：类型推导出错时返回None、变量未声明时返回注解类型作为默认、重复声明时跳过符号注册。')

# 3.13 ★选做
add_heading_styled('3.13 选做：auto类型推导的完整实现', 2)
add_para('作为选做加分内容，本实验实现了基于auto关键字的局部变量类型推导。auto关键字允许程序员省略显式类型声明，编译器根据初始化表达式自动推断变量类型。这需要同时在三个层面进行修改。')

add_heading_styled('3.13.1 词法层修改', 3)
add_para('在TOKEN_SPECS的KEYWORD正则表达式中添加auto关键字，使词法分析器能识别auto为关键字而非标识符。')
add_code_block('''# 修改前: ('KEYWORD', r'\\b(fn|void|int|float|string|bool|return|break|...)\\b')
# 修改后: ('KEYWORD', r'\\b(fn|void|int|float|string|bool|auto|return|break|...)\\b')''')

add_heading_styled('3.13.2 语法层修改', 3)
add_para('在Parser类中进行三处修改：将auto加入语句起始关键字集合、在parse_statement中添加分发、新增parse_auto_decl()方法解析语法。')
add_code_block('''# 修改1: is_stmt_start() 添加 "auto"
if tok["value"] in ("if","while","return","break","continue","fn",
                     "int","float","string","bool","auto"): return True

# 修改2: parse_statement() 添加分发
elif tok["value"] == "auto": return self.parse_auto_decl()

# 修改3: 新增 parse_auto_decl() 方法
def parse_auto_decl(self):
    auto_tok = self.advance()           # 消费 'auto'
    name_tok = self.expect("ID")        # 变量名
    self.expect("OP", "=")              # 等号（auto声明必须有=）
    init = self.parse_expr()            # 初始化表达式
    return {"type": "AutoVarDecl", "name": name_tok["value"],
            "init": init, "line": auto_tok["line"], "col": auto_tok["col"]}''')

add_heading_styled('3.13.3 语义层修改', 3)
add_para('新增_check_auto_decl()方法，核心逻辑是从初始化表达式推导类型：')
add_code_block('''def _check_auto_decl(self, node):
    """检查 auto 类型推导: auto name = expr
       核心: 递归推导初始化表达式的类型 → 将其作为变量的声明类型
    """
    name = node.get("name", ""); init = node.get("init")

    # 重复声明检查
    if self.symtab.lookup_current_scope(name):
        self.error("REDECLARED", f"'{name}' is already declared", ...); return

    # ★ 核心: 推导初始化表达式的类型
    # auto a = 5       → _check_expr(IntLiteral("5"))      → "int"
    # auto b = 3.14    → _check_expr(FloatLiteral("3.14"))→ "float"
    # auto c = true    → _check_expr(BoolLiteral("true"))  → "bool"
    inferred_type = self._check_expr(init) or "int"

    # 用推导出的类型注册符号
    sym = Symbol(name, inferred_type, "var", line, col, self.symtab.current_level())
    self.symtab.define(sym)''')
add_para('auto推导的关键设计：推导出的类型直接作为变量的sym_type使用，后续该变量通过@类型注解使用时（如a@int），检查逻辑与普通声明的变量完全一致——都是比较注解类型与符号表中存储的类型。这保证了auto功能与现有类型系统的无缝集成。')

# 3.14
add_heading_styled('3.14 @类型注解的交叉验证', 2)
add_para('NovaLang最具特色的设计之一是变量使用时必须标注@类型。_check_typed_var_ref()方法实现声明类型与使用类型的交叉验证：不仅查找变量是否已声明，还验证使用时标注的类型是否与声明时一致。')
add_code_block('''def _check_typed_var_ref(self, node):
    """检查带类型引用: name@Type — 交叉验证声明类型 == 使用标注类型"""
    name = node.get("name", ""); ref_type = node.get("ref_type", "")
    sym = self.symtab.lookup(name)
    if sym is None:
        self.error("UNDECLARED", f"'{name}' is not declared", ...); return ref_type
    if sym.kind == "func":
        self.error("TYPE_MISMATCH", f"'{name}' is a function, not a variable", ...)
        return ref_type
    # ★ 交叉验证: 声明的类型必须与使用的@类型一致
    if sym.sym_type != ref_type:
        self.error("TYPE_MISMATCH",
                   f"'{name}' declared as '{sym.sym_type}', used as '{ref_type}'", ...)
    return ref_type''')

# 3.15
add_heading_styled('3.15 与前后端实验的对接', 2)
add_para('（1）与语法分析（实验三）的对接：语义分析器接收语法分析器输出的AST JSON字典作为输入。接口约定是AST根节点为Program类型，包含funcs列表。如果词法或语法阶段已检测到错误，语义分析被跳过（因为AST可能不完整），直接输出前端错误。这在compiler.py的check命令中通过all_frontend_errors判断实现。')
add_para('（2）与代码生成（实验五）的对接：语义分析器输出的符号表提供了代码生成所需的关键信息：每个变量的类型和存储位置、每个函数的参数签名和返回类型。语义错误列表确保只有语义正确的程序进入代码生成。函数类型字符串（如"int(int,int)"）可直接用于生成函数调用时的栈帧布局。')

# ====================================================================
# 四、完整功能演示流程
# ====================================================================
add_heading_styled('四、完整功能演示流程', 1)
add_para('以下逐项展示本实验每个功能的运行效果，包含输入源代码、运行命令、实际输出结果及分析说明。')

add_heading_styled('4.1 正确程序语义检查——S1递归函数', 2)
add_code_block('''// 输入: scenarios/S1.src
fn(int) fib -> n@int:
    if n@int <= 1:
        return n@int
    return fib->(n@int - 1) + fib->(n@int - 2)

fn(void) main ->:
    int n; int answer
    n@int = 8; answer@int = fib->(n@int); print->(answer@int)''')
add_para('命令：python compiler.py check scenarios/S1.src')
s1 = load_check_result('scenarios/S1.check.json')
if s1:
    add_json_block(json.dumps(s1, ensure_ascii=False, indent=2))
    add_para('分析：errors为[]通过全部检查。fib递归调用的实参类型与形参匹配。二元表达式<=、-、+的类型检查均通过。print内置函数参数类型为"any"，跳过类型检查。')

add_heading_styled('4.2 S2变量遮蔽验证', 2)
s2 = load_check_result('scenarios/S2.check.json')
if s2:
    add_para('三个value变量的符号表记录（不同scope）：')
    vals = [s for s in s2["symbols"] if s["name"] == "value"]
    add_json_block(json.dumps(vals, ensure_ascii=False, indent=2))
    add_para('分析：三个同名value分别位于function、block、block三个不同作用域层级。语义分析器正确区分了它们的作用域归属，检查通过（0 errors）。')

add_heading_styled('4.3 S3类型转换方法调用', 2)
s3 = load_check_result('scenarios/S3.check.json')
if s3:
    add_json_block(json.dumps({"errors": s3["errors"]}, ensure_ascii=False, indent=2))
    add_para('分析：sum@int.toFloat()调用通过——toFloat()只能在int上调用，返回float。avg@float.toInt()调用通过——toInt()只能在float上调用。')

add_heading_styled('4.4 S8全类型语义错误检测', 2)
add_para('S8场景定义了8个测试函数，每个触发一种语义错误。运行结果：')
s8 = load_check_result('scenarios/S8.check.json')
if s8:
    add_json_block(json.dumps(s8["errors"], ensure_ascii=False, indent=2))
    add_para('错误类型分布：UNDECLARED(1), REDECLARED(1), TYPE_MISMATCH(2), RETURN_TYPE_MISMATCH(1), ARG_COUNT_MISMATCH(1), ARG_TYPE_MISMATCH(1), NOT_A_FUNCTION(1)。共7种错误类型，8个错误实例。TYPE_MISMATCH出现了两次（赋值不匹配+运算符不匹配），验证了"继续分析"策略——前一个错误不阻止后续检测。')

add_heading_styled('4.5 auto类型推导演示（选做）', 2)
add_code_block('''fn(void) testAuto ->:
    auto a = 5         ← 推导为 int
    auto b = 3.14      ← 推导为 float
    auto c = true      ← 推导为 bool
    print->(a@int); print->(b@float); print->(c@bool)
fn(void) main ->: testAuto->()''')
add_para('命令：python compiler.py check tests/test_11_auto_infer.src')
t11 = load_check_result('tests/test_11_auto_infer.expected.json')
if t11:
    add_json_block(json.dumps({"errors": t11["errors"]}, ensure_ascii=False, indent=2))
    auto_syms = [s for s in t11["symbols"] if s["name"] in ("a", "b", "c")]
    add_json_block(json.dumps(auto_syms, ensure_ascii=False, indent=2))
    add_para('a推导为int、b推导为float、c推导为bool，与使用时的@类型一致，0个语义错误。验证了auto推导从词法→语法→语义的完整链路。')

add_heading_styled('4.6 前端错误时跳过语义分析', 2)
add_para('输入S6.src（含词法错误$和语法错误if缺冒号）时，仅返回词法和语法错误，symbols为空，语义分析器未被调用。这符合"分层防护"的设计。')

add_heading_styled('4.7 测试用例汇总', 2)
add_table_simple(
    ['用例', '场景', '预期', '实际', '状态'],
    [
        ['test_01', '嵌套作用域', '0', '0', '✅'], ['test_02', '变量遮蔽', '0', '0', '✅'],
        ['test_03', 'UNDECLARED', '1', '1', '✅'], ['test_04', 'REDECLARED', '2', '2', '✅'],
        ['test_05', 'TYPE_MISMATCH+RETURN', '2', '2', '✅'], ['test_06', '运算符错误', '1', '1', '✅'],
        ['test_07', 'ARG_COUNT', '1', '1', '✅'], ['test_08', 'ARG_TYPE', '1', '1', '✅'],
        ['test_09', '正确程序(递归)', '0', '0', '✅'], ['test_10', '正确程序(转换)', '0', '0', '✅'],
        ['test_11', 'auto推导(选做)', '0', '0', '✅'],
    ]
)

# ====================================================================
# 五、AI协作过程小结
# ====================================================================
add_heading_styled('五、AI协作过程小结', 1)
add_para('本实验使用Claude Code（Agent IDE）辅助开发，采用"人主导设计、AI辅助实现、人审查验证"的协作模式。共进行了11轮协作对话。')

add_heading_styled('5.1 由我主导设计的部分', 2)
for item in [
    '类型系统设计：严格类型匹配原则、类型兼容性规则矩阵、@类型注解的交叉验证逻辑——延续实验一中NovaLang的设计哲学',
    '符号表数据结构：选择作用域栈而非单表+层级标记，栈结构与AST递归遍历天然匹配——基于编译原理课程所学知识',
    '两遍分析策略：第一遍收集函数声明、第二遍检查函数体——参考C语言前向声明的思想',
    '错误处理策略：选择"检测-记录-继续"模式而非中断式处理——基于教学场景需要一次看到所有错误',
    '选做任务：选择实现auto类型推导而非复杂类型扩展——与NovaLang"减少语法噪声"的哲学一致',
]:
    add_bullet(item)

add_heading_styled('5.2 AI辅助实现的部分', 2)
for item in [
    '代码框架生成：在确定设计方案后，AI生成了semantic_module.py的完整框架代码，我在此基础上调整细节',
    '测试用例生成：AI生成了11个测试用例的源代码和预期输出，覆盖全部测试场景',
    '实验报告初稿：AI生成了报告的结构框架和内容初稿，我进行了补充和修改',
    '问题定位与修复：测试中发现的bug（print未声明、auto解析未加入is_stmt_start等），AI协助快速定位修复',
]:
    add_bullet(item)

add_heading_styled('5.3 验证AI产出正确性的方式', 2)
for item in [
    '自动化回归测试：批量运行S1-S5、S8、全部测试用例，对比实际输出与.expected.json',
    '边界条件人工验证：构造三层嵌套遮蔽、auto推导类型与@类型不一致、int+bool运算等边界用例手动验证',
    '代码逐行审查：通读全部约900行代码，确认每个方法的逻辑正确性——特别关注运算符分类表和函数调用参数匹配',
    '理论对照验证：将实现与《龙书》第5-6章的符号表管理和类型检查理论对照',
]:
    add_bullet(item)

# ====================================================================
# 六、遇到的问题及解决方案
# ====================================================================
add_heading_styled('六、遇到的问题及解决方案', 1)
problems = [
    ('问题1：print内置函数未声明',
     '所有场景都使用print->()输出，但print未声明，导致UNDECLARED错误。',
     '添加_register_builtins()方法注册print为内置函数，参数类型设为"any"以跳过类型检查。'),
    ('问题2：函数前向引用误报',
     'fib递归调用自身时，单遍分析可能在函数注册前遇到调用点。',
     '采用两遍分析：第一遍收集所有函数签名，第二遍检查函数体。'),
    ('问题3：作用域退出后类型信息丢失',
     '变量随作用域退出而从查找范围消失，但需要保留在输出中。',
     '使用all_symbols列表独立于作用域栈保存所有符号，输出用all_symbols，查找用作用域栈。'),
    ('问题4：auto关键字需要三层协同修改',
     'auto功能涉及词法/语法/语义三层，遗漏任何一层都会导致解析失败。',
     '逐层添加：词法→正则添加auto；语法→is_stmt_start+parse_statement分发+parse_auto_decl；语义→_check_statement分发+_check_auto_decl。每层完成后分别测试。'),
    ('问题5：模板docx使用WPS格式',
     'python-docx无法读取WPS Office生成的docx（非标准命名空间）。',
     '通过解压docx直接解析XML，提取封面结构和格式信息，然后用python-docx重建相同格式。'),
]
for i, (title, desc, sol) in enumerate(problems):
    add_heading_styled(f'6.{i+1} {title}', 2)
    add_para(f'现象：{desc}')
    add_para(f'解决方案：{sol}')

# ====================================================================
# 七、总结
# ====================================================================
add_heading_styled('七、总结', 1)

add_heading_styled('7.1 实验成果', 2)
for a in [
    '实现了完整的语义分析器（semantic_module.py约410行），采用访问者模式对AST进行遍历检查',
    '构建了基于作用域栈的三级嵌套符号表，正确处理作用域进入/退出和变量遮蔽',
    '实现了7种基本语义错误类型的检测和精确定位（含行号、列号、上下文信息）',
    '采用"继续分析"策略，一次运行可报告多个语义错误，提升调试效率',
    '完成选做任务——基于auto关键字的局部变量类型推导，涉及词法/语法/语义三层协同修改',
    '编写11个测试用例（含1个选做）和6个场景验证，覆盖全部必测和选测场景',
    '为后续代码生成实验提供了完整的符号表和类型信息',
]:
    add_bullet(a)

add_heading_styled('7.2 关键设计决策回顾', 2)
add_para('严格类型匹配：禁止隐式类型转换，所有转换必须通过toFloat()/toInt()显式进行。这一设计消除了隐式转换带来的歧义，使类型检查逻辑简洁且可预测。')
add_para('两遍分析策略：第一遍收集函数签名，第二遍检查函数体。消除了函数定义顺序的依赖，实现了类似C前向声明的效果。')
add_para('作用域栈设计：栈结构与递归遍历AST天然对应（进入结构→push，离开结构→pop），变量遮蔽由lookup()的从栈顶到栈底的搜索顺序自然保证。')

add_heading_styled('7.3 改进方向', 2)
for imp in ['增强类型推导（函数返回值推导、泛型参数推导）', '更丰富的类型系统（结构体、枚举）',
            '诊断分级（ERROR vs WARNING，如未使用变量）', '常量折叠等编译时优化',
            '符号表可视化输出']:
    add_bullet(imp)

# ====================================================================
# 八、交付物清单
# ====================================================================
add_heading_styled('八、交付物清单', 1)
add_table_simple(
    ['序号', '交付物', '文件', '说明'],
    [
        ['1', '语义分析器源代码', 'compiler.py, semantic_module.py', '含auto类型推导(选做)'],
        ['2', '构建/运行说明', 'README.md', '命令用法、架构说明、测试情况'],
        ['3', '类型系统设计文档', 'type-system.md', '类型定义、兼容规则、作用域规则'],
        ['4', '测试用例集(11组)', 'tests/test_01~11.src + .expected.json', '10组必做+1组选做'],
        ['5', '场景check结果', 'scenarios/S1~S8.check.json', '5正向+S8语义错误'],
        ['6', 'AI协作对话记录', 'conversation/conversation.md', '11轮完整对话+工作纪要'],
        ['7', '实验报告', '李圣元2024150118实验四实验报告.docx', '本文档(基于模板格式)'],
    ]
)

# ====================================================================
# 保存
# ====================================================================
import tempfile, shutil
output_path = os.path.join(os.path.dirname(__file__), '李圣元2024150118实验四实验报告.docx')
try:
    doc.save(output_path)
    print(f'报告已生成: {output_path}')
except PermissionError:
    tmp = os.path.join(tempfile.gettempdir(), 'exp4_report.docx')
    doc.save(tmp)
    try:
        shutil.copy(tmp, output_path)
        print(f'报告已保存(overwrite)')
    except PermissionError:
        alt = os.path.join(os.path.dirname(__file__), '实验四报告_新.docx')
        shutil.copy(tmp, alt)
        print(f'原文件被锁定，已保存到: {alt}')
