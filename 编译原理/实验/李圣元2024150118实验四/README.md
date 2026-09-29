# 实验四：语义分析与类型系统

## 一、概述

本项目在实验三语法分析器的基础上，实现了NovaLang语言的语义分析器（Semantic Analyzer），包括符号表构建、作用域管理和类型检查。

## 二、文件结构

```
实验四/
├── compiler.py              # 主编译器程序（词法+语法+语义）
├── semantic_module.py       # 语义分析器核心模块
├── type-system.md           # 类型系统设计文档
├── README.md                # 本文件
├── scenarios/               # 场景文件
│   ├── S1.src ~ S5.src      # 原有场景（复制自实验一）
│   ├── S8.src               # 语义错误场景
│   └── S1.check.json ~ S8.check.json  # 语义检查结果
├── tests/                   # 测试用例集
│   ├── test_01~10.src       # 测试源文件
│   └── test_01~10.expected.json  # 预期输出
└── conversation/            # AI协作对话记录
```

## 三、构建与运行

本项目使用Python编写，无需编译。

### 1. 运行命令

```bash
# 语义分析（输出语义错误列表和符号表）
python compiler.py check <input.src>

# 词法分析（输出Token序列）
python compiler.py tokenize <input.src>

# 语法分析（输出AST）
python compiler.py parse <input.src>
```

### 2. 输出格式

成功时（无语义错误）：
```json
{
  "errors": [],
  "symbols": [
    {"name": "x", "type": "int", "scope": "global", "line": 1},
    {"name": "f", "type": "int(int,int)", "scope": "global", "line": 3}
  ]
}
```

存在语义错误时：
```json
{
  "errors": [
    {"type": "UNDECLARED", "symbol": "y", "line": 5, "col": 3},
    {"type": "TYPE_MISMATCH", "expected": "int", "found": "string", "line": 6, "col": 7}
  ],
  "symbols": [...]
}
```

### 3. 示例

```bash
# 检查单个场景
python compiler.py check scenarios/S1.src

# 运行所有测试
for f in tests/*.src; do
    python compiler.py check "$f" > "${f%.src}.output.json"
done
```

## 四、架构设计

### 4.1 整体流程

```
源代码 → 词法分析器 → Token序列 → 语法分析器 → AST → 语义分析器 → 符号表 + 错误列表
```

### 4.2 语义分析器核心模块

`semantic_module.py` 包含以下核心类：

- **Symbol**: 符号表条目，记录名称、类型、种类、位置、作用域层级
- **Scope**: 单个作用域，包含符号字典
- **SymbolTable**: 嵌套作用域符号表，支持作用域栈操作
- **SemanticError**: 语义错误信息
- **SemanticAnalyzer**: 语义分析器主类，遍历AST进行语义检查

### 4.3 语义检查流程

1. **第一遍**: 收集所有函数声明（支持前向引用）
2. **第二遍**: 逐函数检查函数体
   - 进入函数作用域，声明参数
   - 遍历语句列表，检查每条语句
   - 对表达式进行类型推导和检查

### 4.4 检测的语义错误类型

| 错误类型 | 说明 |
|----------|------|
| UNDECLARED | 使用未声明的变量/函数 |
| REDECLARED | 同一作用域内重复声明 |
| TYPE_MISMATCH | 类型不兼容（赋值/运算/返回值） |
| ARG_COUNT_MISMATCH | 函数调用参数个数错误 |
| ARG_TYPE_MISMATCH | 函数调用参数类型错误 |
| NOT_A_FUNCTION | 将非函数当作函数调用 |
| RETURN_TYPE_MISMATCH | 返回值类型与函数声明不匹配 |

## 五、测试情况

### 测试用例覆盖

| 编号 | 测试场景 | 用例文件 | 预期 |
|------|----------|----------|------|
| T1-1 | 嵌套作用域 | test_01 | 0 errors |
| T1-2 | 变量遮蔽 | test_02 | 0 errors |
| T2-1 | 未声明变量 | test_03 | 1 error (UNDECLARED) |
| T2-2 | 重复声明 | test_04 | 2 errors (REDECLARED + TYPE_MISMATCH) |
| T3-1 | 类型不匹配 | test_05 | 2 errors (TYPE_MISMATCH + RETURN_TYPE_MISMATCH) |
| T3-2 | 运算符类型错误 | test_06 | 1 error (TYPE_MISMATCH) |
| T4-1 | 参数个数错误 | test_07 | 1 error (ARG_COUNT_MISMATCH) |
| T4-2 | 参数类型错误 | test_08 | 1 error (ARG_TYPE_MISMATCH) |
| T5-1 | 正确程序1 | test_09 | 0 errors |
| T5-2 | 正确程序2（含类型转换） | test_10 | 0 errors |
| T6(选做) | auto类型推导 | test_11 | 0 errors |

### 选做：auto类型推导

支持 `auto name = expr` 语法，编译器根据初始化表达式自动推断变量类型：
- `auto a = 5` → 推导为 int
- `auto b = 3.14` → 推导为 float
- `auto c = true` → 推导为 bool

使用变量时仍需带 @类型注解，注解类型必须与推导类型一致。

### 场景验证

| 场景 | 说明 | 结果 |
|------|------|------|
| S1 | 递归函数（斐波那契） | 0 errors |
| S2 | 嵌套作用域与变量遮蔽 | 0 errors |
| S3 | 类型检查与类型转换 | 0 errors |
| S4 | 控制流嵌套 | 0 errors |
| S5 | 数组操作 | 0 errors |
| S8 | 语义错误示例 | 8 errors (全部7种类型) |
