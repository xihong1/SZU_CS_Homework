# 实验四：语义分析与类型系统 实验报告

## 一、实验概述

本实验是编译原理实验系列的第四个实验。在实验三中，语法分析器已经能够构建抽象语法树（AST）。本实验的目标是：在AST的基础上进行语义分析——构建符号表、管理作用域、进行类型检查，检测并报告各类语义错误。

语法正确的程序未必有意义：变量可能未声明就使用，类型可能不匹配，函数调用参数个数可能错误。语义分析负责在编译期捕获这些错误，是保证程序正确性的重要一环，也是连接前端与后端的桥梁。

## 二、实验目标

- 理解符号表的构建与作用域管理（嵌套作用域、变量遮蔽）
- 掌握类型系统的设计与类型检查的实现
- 能够检测常见的语义错误并准确定位
- 掌握基于AST遍历的语义分析方法（属性文法/访问者模式）

## 三、设计与实现

### 3.1 NovaLang类型系统设计

NovaLang采用**静态强类型**系统，所有变量类型在编译时确定。

**基本类型**：int（整型）、float（浮点型）、string（字符串）、bool（布尔型）、void（空类型，仅用于函数返回值）

**复合类型**：数组类型（如 `int[5]`）、函数类型（如 `int(int,int)`）

**严格匹配原则**：NovaLang不允许隐式类型转换。`int`与`float`即使都是数值类型也不兼容。类型转换必须通过显式方法调用：
- `x@int.toFloat()` → 将int转float
- `x@float.toInt()` → 将float转int

**类型注解设计**：NovaLang要求变量使用时必须标注类型（如 `a@int`），这是该语言的核心特性之一——将类型检查从声明时刻扩展到使用时刻，提升错误定位的可观测性。

### 3.2 符号表与作用域管理

#### 3.2.1 数据结构设计

符号表采用**作用域栈**结构，支持嵌套作用域的进入和退出：

```python
class SymbolTable:
    def __init__(self):
        self.scopes = []        # 作用域栈
        self.all_symbols = []   # 所有已定义符号

    def enter_scope(self):      # 进入新作用域
    def exit_scope(self):       # 退出当前作用域
    def lookup(self, name):     # 从内到外查找符号
    def lookup_current_scope(self, name):  # 仅当前作用域查找
```

每个Symbol条目记录：名称、类型字符串、种类（var/param/func/array）、声明位置、作用域层级。

#### 3.2.2 作用域层级

```
全局作用域 (level 0)     -- 函数声明、内置函数
├── 函数作用域 (level 1) -- 参数 + 局部变量
│   └── 块作用域 (level 2+) -- if/while 块内变量
```

#### 3.2.3 变量遮蔽处理

- 符号查找从最内层作用域向外层搜索
- 内层可以声明与外层同名的变量，形成合法遮蔽
- 同一作用域内禁止重复声明

在实现中，每次进入if/while语句块时调用`enter_scope()`，退出时调用`exit_scope()`，使得块内变量自动形成新的遮蔽层。

### 3.3 语义检查实现

#### 3.3.1 分析策略

采用基于AST遍历的**访问者模式**，对每种AST节点实现对应的检查方法。分析分为两遍：

**第一遍**：收集所有函数声明，建立函数签名表，支持函数间的相互调用（前向引用）。

```python
def check(self, ast):
    self.symtab.enter_scope()    # 全局作用域
    self._register_builtins()    # 注册内置函数

    # 第一遍：声明所有函数
    for func in funcs:
        self._declare_function(func)

    # 第二遍：检查函数体
    for func in funcs:
        self._check_function(func)
```

**第二遍**：逐个函数检查函数体，包括：
- 进入函数作用域，声明参数
- 遍历每条语句进行语义检查
- 对表达式进行递归类型推导

#### 3.3.2 类型推导

表达式类型推导是递归的：叶子节点返回基本类型，内部节点根据运算符和子节点类型计算整体类型。例如：

- `IntLiteral` → `"int"`
- `FloatLiteral` → `"float"`
- `BinaryExpr(op="+", int, int)` → `"int"`
- `BinaryExpr(op="<", int, int)` → `"bool"`
- `CallExpr(func_name, args)` → 函数的返回类型
- `MethodCall(method="toFloat", obj_type="int")` → `"float"`

#### 3.3.3 错误检测实现

**UNDECLARED（未声明）**：在查找符号时，若`lookup()`返回None则报告错误。

**REDECLARED（重复声明）**：在声明变量/函数前，调用`lookup_current_scope()`检查是否已存在同名符号。

**TYPE_MISMATCH（类型不匹配）**：在赋值时比较左右类型；在二元运算时检查操作数类型一致性和运算符合法性。

**ARG_COUNT_MISMATCH（参数个数错误）**：比较函数调用实参数量与形参数量。

**ARG_TYPE_MISMATCH（参数类型错误）**：逐个比较实参类型与形参类型。

**NOT_A_FUNCTION（非函数调用）**：检查被调用符号的kind是否为`"func"`。

**RETURN_TYPE_MISMATCH（返回值类型错误）**：比较return表达式的类型与函数声明的返回类型。

### 3.4 错误定位与恢复

每个语义错误都包含精确的行号和列号，便于定位。语义分析器采用**继续分析**策略：
- 遇到语义错误时记录错误信息
- 继续分析后续AST节点
- 一次运行报告所有语义错误

这样设计的好处是开发者可以一次看到所有语义错误，而不需要逐个修复再重新编译。

### 3.5 整体架构

```
compiler.py (主程序)
├── tokenize() - 词法分析器
├── Parser类 - 语法分析器（递归下降）
└── semantic_module.py (语义分析器)
    ├── Symbol - 符号表条目
    ├── Scope - 单个作用域
    ├── SymbolTable - 嵌套作用域符号表
    ├── SemanticError - 语义错误
    └── SemanticAnalyzer - 语义分析器主类
        ├── _check_function()   - 函数体检查
        ├── _check_statement()  - 语句分发
        ├── _check_var_decl()   - 变量声明检查
        ├── _check_assign()     - 赋值检查
        ├── _check_if()         - if语句检查
        ├── _check_while()      - while语句检查
        ├── _check_return()     - return检查
        ├── _check_expr()       - 表达式分发
        ├── _check_binary_expr()- 二元表达式检查
        ├── _check_call_expr()  - 函数调用检查
        └── _check_method_call()- 方法调用检查
```

## 四、测试结果

### 4.1 场景测试

| 场景 | 说明 | 错误数 | 结果 |
|------|------|--------|------|
| S1.src | 递归函数（斐波那契） | 0 | 通过 |
| S2.src | 嵌套作用域与变量遮蔽 | 0 | 通过 |
| S3.src | 类型检查与类型转换 | 0 | 通过 |
| S4.src | 控制流嵌套（if与while） | 0 | 通过 |
| S5.src | 数组操作 | 0 | 通过 |
| S8.src | 语义错误示范 | 8 | 正确检测全部8个错误 |

**S8错误详细分析**：

| 行号 | 错误类型 | 说明 |
|------|----------|------|
| 7 | UNDECLARED | 使用未声明的变量 y |
| 12 | REDECLARED | 同一作用域重复声明 x |
| 19 | TYPE_MISMATCH | 将string赋值给int |
| 25 | RETURN_TYPE_MISMATCH | 返回string但声明为int |
| 33 | ARG_COUNT_MISMATCH | add需要2个参数，只给了1个 |
| 40 | ARG_TYPE_MISMATCH | add第1个参数期望int，给了string |
| 46 | NOT_A_FUNCTION | 将变量x当作函数调用 |
| 54 | TYPE_MISMATCH | 算术运算符+的操作数类型不匹配 |

### 4.2 测试用例

| 测试 | 覆盖场景 | 错误数 | 结果 |
|------|----------|--------|------|
| test_01 | 嵌套作用域 | 0 | 通过 |
| test_02 | 变量遮蔽 | 0 | 通过 |
| test_03 | 未声明变量 | 1 | 通过 |
| test_04 | 重复声明 | 2 | 通过 |
| test_05 | 类型不匹配 | 2 | 通过 |
| test_06 | 运算符类型错误 | 1 | 通过 |
| test_07 | 参数个数错误 | 1 | 通过 |
| test_08 | 参数类型错误 | 1 | 通过 |
| test_09 | 正确程序1（递归） | 0 | 通过 |
| test_10 | 正确程序2（类型转换） | 0 | 通过 |

## 五、示例演示

### 5.1 正确程序示例

输入（test_09_correct1.src - 阶乘函数）：
```nova
fn(int) factorial -> n@int:
    if n@int <= 1:
        return 1
    return n@int * factorial->(n@int - 1)

fn(void) main ->:
    int result
    result@int = factorial->(5)
    print->(result@int)
```

运行命令：
```bash
python compiler.py check tests/test_09_correct1.src
```

输出：
```json
{
  "errors": [],
  "symbols": [
    { "name": "print", "type": "void(any)", "scope": "global", "line": 0 },
    { "name": "factorial", "type": "int(int)", "scope": "global", "line": 1 },
    { "name": "main", "type": "void()", "scope": "global", "line": 6 },
    { "name": "n", "type": "int", "scope": "function", "line": 1 },
    { "name": "result", "type": "int", "scope": "function", "line": 7 }
  ]
}
```

### 5.2 错误程序示例

输入（S8场景局部 - 参数类型错误）：
```nova
fn(int) add -> a@int, b@int:
    return a@int + b@int

fn(void) testArgType ->:
    int x
    string s
    s@string = "world"
    x@int = add->(s@string, 2)   // 错误：string传入int参数
```

输出：
```json
{
  "errors": [
    { "type": "ARG_TYPE_MISMATCH", "line": 8, "col": 13,
      "symbol": "add", "expected": "int", "found": "string" }
  ],
  "symbols": [...]
}
```

### 5.3 嵌套作用域与变量遮蔽验证

输入（S2场景）展示了三个嵌套的`value`变量，语义分析正确识别了每种作用域中的变量声明和使用。符号表输出了三个不同作用域的`value`符号，分别标记为function和block作用域，证明了作用域管理和变量遮蔽的正确处理。

## 六、遇到的问题及解决方案

### 问题1：print函数未声明
**现象**：所有场景程序都使用`print->()`输出，但print未在任何地方声明
**原因**：print是NovaLang的隐式内置函数，语法和词法规范中没有要求显式声明
**解决**：在语义分析器中添加`_register_builtins()`方法，将print注册为接受任意类型参数（`any`类型）的内置函数，返回void

### 问题2：参数类型的any匹配
**现象**：内置函数print接受任意类型，但普通函数需要严格类型匹配
**解决**：在参数类型检查中增加对`"any"`类型的特殊处理——当期望类型为`"any"`时跳过类型检查

### 问题3：函数声明的两遍分析
**现象**：函数间可能存在相互调用或前向引用，单遍分析会导致函数未被声明
**解决**：采用两遍分析策略——第一遍仅收集所有函数签名并注册到全局符号表，第二遍再进行函数体的语义检查。这类似于C/C++中的前向声明机制。

### 问题4：错误恢复与继续分析
**现象**：如何在一个错误后继续分析后续代码而不让整个分析中断
**解决**：语义分析器在每个检查方法中都采用"检查-记录-继续"的模式：发现错误时不抛出异常，而是调用`self.error()`记录错误并继续遍历AST。类型推导在出错时返回None（而不是中断），使得后续分析可以继续进行。

## 七、总结

### 7.1 实验成果

1. 实现了完整的语义分析器，支持NovaLang所有语义检查需求
2. 构建了嵌套作用域符号表，正确处理作用域进入退出和变量遮蔽
3. 实现了7种语义错误的检测和精准定位
4. 支持一次分析报告多个语义错误，提升开发体验
5. 生成规范的JSON输出，为后续实验（代码生成）打下基础

### 7.2 设计决策

1. **严格类型匹配**：禁止隐式类型转换，所有类型转换必须通过显式方法调用。这与NovaLang"安全透明"的设计哲学一致。
2. **两遍分析**：第一遍收集函数签名，第二遍检查函数体。这平衡了实现复杂度和前向引用支持。
3. **继续分析策略**：发现错误后继续分析，一次报告所有错误。这对教学和调试特别重要。
4. **访问者模式**：每种AST节点对应一个检查方法，代码结构清晰，易于扩展和维护。

### 7.3 改进方向

1. 可以支持更丰富的类型系统（如结构体、枚举）
2. 可以增加类型推导功能（根据初始化表达式自动推断变量类型）
3. 可以添加未使用变量的警告（WARNING级别）
4. 可以增强符号表的可视化输出

## 八、交付物清单

| 序号 | 交付物 | 文件 | 说明 |
|------|--------|------|------|
| 1 | 语义分析器源代码 | compiler.py, semantic_module.py | Python实现 |
| 2 | 构建/运行说明 | README.md | 如何编译和运行 |
| 3 | 类型系统设计文档 | type-system.md | 类型定义与兼容规则 |
| 4 | 测试用例集 | tests/test_01~10.src + .expected.json | 10组测试用例 |
| 5 | 场景check结果 | scenarios/S1~S8.check.json | 5个正向+1个语义错误 |
| 6 | AI协作对话记录 | conversation/ | 完整对话+工作纪要 |
| 7 | 实验报告 | report.md | 本报告 |
