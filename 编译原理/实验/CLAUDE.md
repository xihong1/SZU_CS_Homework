# 编译原理实验 — NovaLang 编译器项目

## 项目概述

为编译原理课程设计的完整编译器，语言名为 **NovaLang**，使用 Python 实现。已完成实验一至四（语言设计→词法分析→语法分析→语义分析），即将进入实验五（代码生成）。

- **姓名**: 李圣元
- **学号**: 2024150118

---

## NovaLang 语言特性速览

### 基本语法（Python风格缩进块）

```
fn(返回类型) 函数名 -> 参数列表:
    语句块（缩进4空格）

fn(void) main ->:          ← 程序入口（必须此形式）
```

### 类型系统（静态强类型，严格匹配，禁止隐式转换）

| 类型 | 关键字 | 说明 |
|------|--------|------|
| 整型 | `int` | |
| 浮点 | `float` | |
| 字符串 | `string` | |
| 布尔 | `bool` | `true` / `false` |
| 空 | `void` | 仅函数返回 |

### 核心语法规则

```nova
// 变量声明：类型 变量名
int a
int a[5]            // 数组声明
int a = 5           // 声明+初始化（类型必须匹配）
auto a = 5          // 类型推导（选做）

// 变量使用：变量名@类型（强制标注，交叉验证）
a@int = 10
a[0]@int = 1        // 数组元素访问
arr@int[5]          // 数组整体引用（传参用）

// 函数定义与调用（箭头风格）
fn(int) add -> a@int, b@int:    // 定义
    return a@int + b@int
add->(1, 2)                     // 调用

// 类型转换（禁止C风格强转，必须方法调用）
x@int.toFloat()     // int → float
x@float.toInt()     // float → int

// 控制流
if cond: ... else: ...    // 冒号+缩进块
while cond: ...
return [expr]
break / continue

// 运算符（对齐C++17）
算术: + - * / %     // %仅int
关系: < <= > >=
相等: == !=
逻辑: && || !
```

### 运算符优先级（从低到高）

1. `||`（逻辑或）
2. `&&`（逻辑与）
3. `==` `!=`（相等）
4. `<` `<=` `>` `>=`（关系）
5. `+` `-`（加减）
6. `*` `/` `%`（乘除模）
7. `!` `-`（一元）

---

## 项目结构

```
实验/
├── CLAUDE.md                          ← 本文件
├── 李圣元2024150118实验一/
│   ├── grammar.ebnf                   ← 语言文法定义（权威参考）
│   ├── decisions.md                   ← 8项设计决策记录
│   ├── scenarios/S1~S6.src            ← 必考场景源程序
│   └── src/main.cpp                   ← 文法分析器（C++）
├── 李圣元2024150118实验二/
│   └── compiler.py                    ← 词法分析器
├── 李圣元2024150118实验三/
│   ├── compiler.py                    ← 词法+语法分析器（含INDENT/DEDENT）
│   ├── parser_module.py               ← 递归下降语法分析器
│   └── ast-design.md                  ← AST节点定义文档
├── 李圣元2024150118实验四/            ★ 当前最新代码
│   ├── compiler.py                    ← 主编译器（tokenize / parse / check）
│   ├── semantic_module.py             ← 语义分析器（符号表+类型检查）
│   ├── type-system.md                 ← 类型系统设计文档
│   ├── tests/test_01~11.src           ← 11组测试用例
│   └── scenarios/S1~S8.src            ← 场景文件 + check结果
└── 李圣元2024150118实验五/            ← 待开发
```

---

### 命令行接口

```bash
python compiler.py tokenize input.src   # 词法分析 → Token序列
python compiler.py parse input.src      # 语法分析 → AST
python compiler.py check input.src      # 语义分析 → 符号表 + 语义错误
```

### 编译器架构

```
compiler.py
├── TOKEN_SPECS            # 17种Token正则（含auto关键字）
├── tokenize_raw()         # 原始词法分析
├── add_indent_tokens()    # INDENT/DEDENT伪Token生成（缩进栈算法）
├── tokenize()             # 完整词法分析入口
├── Parser                 # 递归下降语法分析器
│   ├── parse_program() / parse_function_def()
│   ├── parse_var_decl() / parse_auto_decl()  ★选做
│   ├── parse_statement() 分发中心
│   ├── parse_expr() → 9层优先级链
│   └── parse() → {ast, errors}
└── main()                 # 命令行入口

semantic_module.py
├── Symbol                 # 符号表条目 (name/type/kind/scope_level)
├── Scope                  # 单个作用域 (symbols字典)
├── SymbolTable            # 作用域栈 (enter/exit/lookup/lookup_current)
├── SemanticError          # 语义错误 (type/line/col/extra)
└── SemanticAnalyzer       # 访问者模式
    ├── check()            # 两遍分析: 先收集函数签名, 再检查函数体
    ├── _check_statement() # 语句分发 (VarDecl/Assign/If/While/Return/...)
    ├── _check_expr()      # 表达式类型推导 (返回类型字符串)
    ├── _check_binary_expr() # 四类运算符约束检查
    ├── _check_call_expr()   # 函数调用: 参数个数+类型
    ├── _check_method_call() # toFloat/toInt 方法检查
    ├── _check_var_decl()    # 四步: 验证类型→查重→注册→检查init
    ├── _check_if()/_check_while() # 含作用域enter/exit
    └── _check_return()      # 返回类型匹配
```

### 检测的7种语义错误

| 错误类型 | 触发条件 |
|----------|---------|
| `UNDECLARED` | lookup() 返回 None |
| `REDECLARED` | lookup_current_scope() 已有同名 |
| `TYPE_MISMATCH` | 赋值左右类型不一致 / 运算符操作数非法 |
| `RETURN_TYPE_MISMATCH` | return_expr_type ≠ 函数声明返回类型 |
| `ARG_COUNT_MISMATCH` | len(args) ≠ len(params) |
| `ARG_TYPE_MISMATCH` | 实参类型 ≠ 对应形参类型 |
| `NOT_A_FUNCTION` | 被调用者 kind ≠ "func" |

---

## 关键设计决策（来自实验一 decisions.md）

1. **缩进块**替代花括号/分号 → 需要 INDENT/DEDENT 伪Token
2. **@类型注解**强制标注 → 声明类型与使用类型交叉验证
3. **禁止C风格强转** → 仅允许 toFloat()/toInt() 方法转换
4. **箭头风格**函数定义/调用 → `fn(ret) name -> params:` / `name->(args)`
5. **数组双形态** → 声明 `int a[5]` / 元素 `a[0]@int` / 整体 `a@int[5]`
6. **入口约束** → `fn(void) main ->:` 固定形式
7. **运算符对齐C++** → 减少学习成本

---

## AST 节点类型（供实验五参考）

| 节点 | type字段 | 关键子字段 |
|------|---------|-----------|
| 程序 | `Program` | funcs: [FuncDecl] |
| 函数声明 | `FuncDecl` | name, return_type, params, body |
| 变量声明 | `VarDecl` | var_type, name, [size], [init] |
| auto声明 | `AutoVarDecl` | name, init（选做） |
| 赋值 | `AssignStmt` | target: TypedVarRef, value: Expr |
| 条件 | `IfStmt` | cond, then, [else] |
| 循环 | `WhileStmt` | cond, body |
| 返回 | `ReturnStmt` | [expr] |
| 二元表达式 | `BinaryExpr` | op, left, right |
| 一元表达式 | `UnaryExpr` | op, operand |
| 函数调用 | `CallExpr` | callee: Identifier, args |
| 方法调用 | `MethodCall` | object, method, args |
| 类型引用 | `TypedVarRef` | name, ref_type（如 "int"） |
| 数组元素引用 | `TypedArrayElemRef` | name, index, ref_type |
| 数组整体引用 | `TypedArrayRef` | name, ref_type, size |
| 字面量 | `IntLiteral`等 | value |

所有节点均带 `line` / `col` 位置信息。

---

## 实验五开发提示

### 可用资源
- **符号表**：`check` 命令输出的 `symbols` 数组包含所有变量/函数的完整类型信息
- **AST**：`parse` 命令输出的完整抽象语法树
- **语义保证**：`check` 通过后程序无语义错误，代码生成无需再做类型验证
- **函数类型字符串**：如 `"int(int,int)"` 可直接解析为参数类型列表和返回类型

### 需要注意的NovaLang特性
- 变量使用时的 `@类型` 注解（TypedVarRef.ref_type 字段）
- 数组的三种形态（声明/元素访问/整体引用）
- 类型转换方法调用（toFloat/toInt）
- 缩进块结构（AST已平化为body列表，无需处理INDENT/DEDENT）
- print 是内置函数（参数类型 `any`，返回 `void`）
- auto 声明的变量（选做，kind为"var"，类型由推导得出）

### 场景验证文件
- S1~S5：正确程序（供生成目标代码）
- S8：语义错误（不应进入代码生成）
- 测试用例 tests/：11个涵盖各特性
