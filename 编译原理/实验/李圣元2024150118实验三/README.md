# 实验三：语法分析

## 一、概述

本项目实现了NovaLang语言的语法分析器（Parser），将词法分析器输出的Token序列构建为抽象语法树（AST），并对语法错误进行检测、定位与恢复。

## 二、文件结构

- `compiler.py`: 主程序，包含词法分析器和命令行接口
- `parser_module.py`: 语法分析器核心实现（递归下降分析）
- `tests/`: 测试用例集（10组）
- `S1.src` ~ `S6.src`: 必考场景程序

## 三、构建与运行

本项目使用Python编写，无需编译。

### 1. 运行命令

```bash
# 词法分析（输出Token序列）
python compiler.py tokenize <input.src>

# 语法分析（输出AST）
python compiler.py parse <input.src>
```

### 2. 示例

```bash
# 解析S1场景
python compiler.py parse scenarios/S1.src

# 解析测试用例

python compiler.py parse tests/test_01_expr_precedence.src
```

## 四、AST节点类型

| 节点类型 | 说明 |
|----------|------|
| Program | 程序根节点，包含函数定义列表 |
| FuncDecl | 函数声明 |
| ParamDecl | 参数声明 |
| VarDecl | 变量声明 |
| AssignStmt | 赋值语句 |
| IfStmt | 条件语句 |
| WhileStmt | 循环语句 |
| ReturnStmt | 返回语句 |
| BreakStmt | break语句 |
| ContinueStmt | continue语句 |
| ExprStmt | 表达式语句 |
| BinaryExpr | 二元表达式 |
| UnaryExpr | 一元表达式 |
| CallExpr | 函数调用 |
| Identifier | 标识符 |
| TypedVarRef | 带类型引用（如 n@int） |
| TypedArrayRef | 数组引用（如 a@int[5]） |
| TypedArrayElemRef | 数组元素引用（如 a[0]@int） |
| IntLiteral | 整数字面量 |
| FloatLiteral | 浮点数字面量 |
| StringLiteral | 字符串字面量 |
| BoolLiteral | 布尔字面量 |

## 五、运算符优先级

从高到低：
1. `!`, `-` (一元)
2. `*`, `/`, `%` (乘除模)
3. `+`, `-` (加减)
4. `<`, `<=`, `>`, `>=` (关系)
5. `==`, `!=` (相等)
6. `&&` (逻辑与)
7. `||` (逻辑或)

## 六、错误恢复策略

采用panic-mode错误恢复：
1. 当遇到语法错误时，记录错误信息
2. 跳过Token直到遇到同步符号（NEWLINE、EOF、DEDENT）
3. 继续分析后续内容，尽可能多地报告错误

## 七、测试情况

已生成10个测试用例，覆盖：
- T1: 表达式优先级与结合性（2组）
- T2: 各类语句（2组）
- T3: 嵌套结构（2组）
- T4: 函数定义与调用（1组）
- T5: 语法错误检测（3组）
