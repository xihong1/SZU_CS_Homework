# 实验三：语法分析 实验报告

## 一、实验概述

本实验是编译原理实验系列的第三个实验。在实验二中，我已经实现了词法分析器，能够将源代码转换为Token序列。本实验的目标是：在此基础上实现语法分析器（Parser），将Token序列按照语言的文法构建为抽象语法树（AST），并对语法错误进行检测、定位与恢复。

## 二、实验目标

- 理解自顶向下（递归下降）语法分析的基本原理
- 掌握上下文无关文法到语法分析器的实现方法
- 正确处理表达式的运算符优先级与结合性
- 能够构建抽象语法树（AST），并设计清晰的AST节点表示
- 实现语法错误的检测、定位与恢复

## 三、设计与实现

### 3.1 语法分析方法选择

**选择方法**：递归下降分析法（Recursive Descent Parsing）

**选择理由**：
1. NovaLang的BNF文法适合LL分析，每个产生式左部都是单个非终结符
2. 递归下降实现直观，每个语法产生式对应一个解析函数
3. 错误恢复容易实现，可以在任何解析函数中捕获异常
4. 与Python的缩进块结构天然契合

**实现架构**：
```
compiler.py (主程序)
├── tokenize() - 词法分析器（扩展支持INDENT/DEDENT）
└── parser_module.py (语法分析器)
    ├── parse_program() - 程序入口
    ├── parse_function_def() - 函数定义
    ├── parse_statement_list() - 语句列表
    ├── parse_statement() - 语句分发
    ├── parse_if_stmt() - if语句
    ├── parse_while_stmt() - while语句
    ├── parse_return_stmt() - return语句
    ├── parse_var_decl() - 变量声明
    ├── parse_id_statement() - 标识符语句（赋值/表达式）
    └── parse_expr() - 表达式解析（优先级递归）
```

### 3.2 Tokenizer扩展

原词法分析器不产生INDENT/DEDENT token，但grammar.ebnf需要它们。我扩展了tokenizer：

```python
def add_indent_tokens(raw_tokens):
    result = []
    indent_stack = [0]  # 缩进栈
    after_newline = True
    
    for tok in raw_tokens:
        if tok["type"] == "NEWLINE":
            result.append(tok)
            after_newline = True
            continue
        
        if after_newline:
            after_newline = False
            indent = compute_indent(tok)  # 计算当前缩进
            current_indent = indent_stack[-1]
            
            if indent > current_indent:
                indent_stack.append(indent)
                result.append({"type": "INDENT", ...})
            elif indent < current_indent:
                while indent_stack[-1] > indent:
                    indent_stack.pop()
                    result.append({"type": "DEDENT", ...})
        
        result.append(tok)
    
    # 文件结束时关闭所有缩进块
    while len(indent_stack) > 1:
        indent_stack.pop()
        result.append({"type": "DEDENT", ...})
    
    return result
```

### 3.3 运算符优先级处理

NovaLang的运算符优先级从高到低：
1. `!`, `-` (一元运算符)
2. `*`, `/`, `%` (乘除模)
3. `+`, `-` (加减)
4. `<`, `<=`, `>`, `>=` (关系)
5. `==`, `!=` (相等)
6. `&&` (逻辑与)
7. `||` (逻辑或)

**实现方式**：每个优先级对应一个解析函数，高优先级的函数先被调用：

```python
def parse_expr(self):
    return self.parse_logical_or()      # 最低优先级

def parse_logical_or(self):
    left = self.parse_logical_and()     # 调用下一级
    while self.peek() == "||":
        self.advance()
        right = self.parse_logical_and()
        left = BinaryExpr("||", left, right)
    return left

def parse_logical_and(self):
    left = self.parse_equality()
    while self.peek() == "&&":
        self.advance()
        right = self.parse_equality()
        left = BinaryExpr("&&", left, right)
    return left
# ... 以此类推到 parse_unary()
```

**结合性处理**：所有二元运算符都是左结合，通过while循环实现：
```python
# a - b - c 解析为 (a - b) - c
def parse_additive(self):
    left = self.parse_multiplicative()
    while self.peek() in ("+", "-"):
        op = self.advance()
        right = self.parse_multiplicative()
        left = BinaryExpr(op, left, right)  # 左结合
    return left
```

### 3.4 AST节点设计

AST节点设计遵循以下原则：
1. 每个节点必须包含 `type` 字段标识节点类型
2. 保留位置信息（line, col）
3. 同类结构生成一致的节点形态

**主要节点类型**：

| 节点类型 | 说明 | 示例 |
|----------|------|------|
| Program | 程序根节点 | 包含funcs列表 |
| FuncDecl | 函数声明 | name, return_type, params, body |
| VarDecl | 变量声明 | var_type, name, size?, init? |
| AssignStmt | 赋值语句 | target, value |
| IfStmt | 条件语句 | cond, then, else? |
| WhileStmt | 循环语句 | cond, body |
| ReturnStmt | 返回语句 | expr? |
| BinaryExpr | 二元表达式 | op, left, right |
| UnaryExpr | 一元表达式 | op, operand |
| CallExpr | 函数调用 | callee, args |
| TypedVarRef | 带类型引用 | name, ref_type |

### 3.5 错误恢复策略

采用 **panic-mode错误恢复**：

1. **检测错误**：当token不匹配预期时，抛出ParseError异常
2. **记录错误**：将错误信息添加到errors列表
3. **恢复分析**：跳过token直到遇到同步符号
4. **继续解析**：尝试解析后续内容

**同步符号**：NEWLINE、EOF、DEDENT

```python
def recover_to_sync(self):
    """跳过token直到遇到同步符号"""
    while self.peek()["type"] not in ("NEWLINE", "EOF", "DEDENT"):
        self.advance()

def parse_statement_list(self):
    stmts = []
    while True:
        if self.peek()["type"] in ("DEDENT", "EOF"):
            break
        if self.peek()["type"] == "NEWLINE":
            self.advance()
            continue
        if not self.is_stmt_start():
            break
        try:
            stmts.append(self.parse_statement())
        except ParseError as e:
            self.error(e.expected, self.peek())  # 记录错误
            self.recover_to_sync()               # 恢复
            self.skip_newlines()                 # 跳过换行
    return stmts
```

## 四、测试结果

### 4.1 场景测试

| 场景 | 说明 | 函数数 | 错误数 | 结果 |
|------|------|--------|--------|------|
| S1.src | 递归函数（斐波那契） | 2 | 0 | OK |
| S2.src | 嵌套作用域与变量遮蔽 | 2 | 0 | OK |
| S3.src | 类型检查与类型转换 | 2 | 0 | OK |
| S4.src | 控制流嵌套（if与while） | 2 | 0 | OK |
| S5.src | 数组操作 | 2 | 0 | OK |
| S6.src | 错误程序示范 | 3 | 2 | ERRORS |

**S6错误分析**：
- 错误1：ILLEGAL_CHAR - 非法字符 `$`（词法错误）
- 错误2：SYNTAX_ERROR - `if`语句缺少冒号（语法错误）

### 4.2 测试用例

| 测试 | 覆盖场景 | 函数数 | 错误数 | 结果 |
|------|----------|--------|--------|------|
| test_01 | 表达式优先级 | 2 | 0 | OK |
| test_02 | 表达式结合性 | 2 | 0 | OK |
| test_03 | 变量声明与赋值 | 1 | 0 | OK |
| test_04 | if/while语句 | 1 | 0 | OK |
| test_05 | 嵌套块结构 | 2 | 0 | OK |
| test_06 | 函数定义与调用 | 3 | 0 | OK |
| test_07 | 语法错误(缺冒号) | 1 | 1 | ERRORS |
| test_08 | 语法错误(缺括号) | 1 | 1 | ERRORS |
| test_09 | 无效语句 | 1 | 0 | OK |
| test_10 | 嵌套表达式 | 2 | 0 | OK |

## 五、示例演示

### 5.1 输入示例

```nova
fn(int) fib -> n@int:
    if n@int <= 1:
        return n@int
    return fib->(n@int - 1) + fib->(n@int - 2)

fn(void) main ->:
    int n
    n@int = 8
    print->(fib->(n@int))
```

### 5.2 输出AST

```json
{
  "ast": {
    "type": "Program",
    "funcs": [
      {
        "type": "FuncDecl",
        "name": "fib",
        "return_type": "int",
        "params": [
          {"type": "ParamDecl", "name": "n", "param_type": "int"}
        ],
        "body": [
          {
            "type": "IfStmt",
            "cond": {
              "type": "BinaryExpr",
              "op": "<=",
              "left": {"type": "TypedVarRef", "name": "n", "ref_type": "int"},
              "right": {"type": "IntLiteral", "value": "1"}
            },
            "then": [
              {"type": "ReturnStmt", "expr": {"type": "TypedVarRef", "name": "n", "ref_type": "int"}}
            ],
            "else": null
          },
          {
            "type": "ReturnStmt",
            "expr": {
              "type": "BinaryExpr",
              "op": "+",
              "left": {
                "type": "CallExpr",
                "callee": {"type": "Identifier", "name": "fib"},
                "args": [{"type": "BinaryExpr", "op": "-", "left": {"type": "TypedVarRef", "name": "n", "ref_type": "int"}, "right": {"type": "IntLiteral", "value": "1"}}]
              },
              "right": {
                "type": "CallExpr",
                "callee": {"type": "Identifier", "name": "fib"},
                "args": [{"type": "BinaryExpr", "op": "-", "left": {"type": "TypedVarRef", "name": "n", "ref_type": "int"}, "right": {"type": "IntLiteral", "value": "2"}}]
              }
            }
          }
        ]
      }
    ]
  },
  "errors": []
}
```

## 六、遇到的问题及解决方案

### 问题1：无限循环
**现象**：parse_statement_list在处理连续NEWLINE时陷入无限循环
**原因**：循环条件判断不完整，未正确处理blank line
**解决**：重构parse_statement_list，在遇到DEDENT/EOF时直接break

### 问题2：函数参数解析错误
**现象**：带参数的函数定义解析失败
**原因**：parse_param_list_opt错误地将冒号放在参数列表中解析
**解决**：将冒号移回调用处解析，参数列表只解析ID开头的参数

### 问题3：数组参数不支持
**现象**：`arr@int[5]`格式的参数解析失败
**原因**：parse_param_decl未处理数组大小
**解决**：添加数组大小解析逻辑

### 问题4：错误恢复不完善
**现象**：语法错误后无法继续解析
**原因**：parse_block_body在错误发生后无法正确跳过到DEDENT
**解决**：在parse_block_body中添加容错逻辑，跳过非DEDENT token

## 七、总结

### 7.1 实验成果

1. 实现了完整的语法分析器，支持NovaLang所有语法结构
2. 正确处理运算符优先级和结合性
3. 实现了语法错误检测和panic-mode错误恢复
4. 生成了规范的AST输出，为后续实验打下基础

### 7.2 设计决策

1. 选择递归下降分析法，实现简单且易于调试
2. 扩展tokenizer支持INDENT/DEDENT，与Python缩进块结构兼容
3. 采用panic-mode错误恢复，平衡了错误报告和实现复杂度

### 7.3 改进方向

1. 可以添加更精确的错误恢复策略（如同步符号集）
2. 可以支持更丰富的错误信息（如期望的token列表）
3. 可以添加AST到图形化表示的转换（如Graphviz DOT格式）

## 八、交付物清单

| 序号 | 交付物 | 文件 | 说明 |
|------|--------|------|------|
| 1 | 语法分析器源代码 | compiler.py, parser_module.py | Python实现 |
| 2 | 构建/运行说明 | README.md | 如何编译和运行 |
| 3 | AST节点定义文档 | ast-design.md | 节点类型与结构说明 |
| 4 | 测试用例集 | tests/*.src + *.expected.json | 10组测试用例 |
| 5 | 场景parse结果 | S1-S6.ast.json | AST输出文件 |
| 6 | AI协作对话记录 | conversation.md | 完整对话+工作纪要 |
| 7 | 实验报告 | report.docx | 本报告 |
