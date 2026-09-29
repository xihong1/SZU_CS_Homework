# 实验四 AI 协作对话记录

## 概述

本实验使用 Claude Code（Agent IDE）辅助开发。以下记录每一轮协作的完整过程：
(1) 我向智能体提出的问题或指令；
(2) 智能体的完整响应（摘要）；
(3) 该轮的工作纪要——我做了什么决策、为什么这样做、如何验证结果。

---

## 第一轮：实验需求分析

**我的指令**：
"帮我读取实验四的题目要求PDF，理解本次实验的目标和交付物清单。"

**智能体响应**：
通过pdftotext成功提取了PDF内容。实验四要求实现语义分析与类型系统，包括：
- 命令行接口：`./compiler check input.src`
- 输出JSON格式（errors + symbols）
- 7种必检语义错误类型：UNDECLARED, REDECLARED, TYPE_MISMATCH, ARG_COUNT_MISMATCH, ARG_TYPE_MISMATCH, NOT_A_FUNCTION, RETURN_TYPE_MISMATCH
- 必做功能：符号表与作用域管理、声明检查、类型检查、错误定位与恢复
- 测试用例 ≥10组，场景S1-S5通过、S8检测语义错误
- 选做任务：类型推导或复杂类型
- 交付物：源代码、README、类型系统文档、测试用例、场景check结果、对话记录、实验报告

**工作纪要**：
- 决策：需要在实验三的compiler.py基础上，新增semantic_module.py实现语义分析功能
- 决策理由：模块化设计，语义分析逻辑独立，便于维护和扩展
- 验证：已将所有必做要求记录为待办事项

---

## 第二轮：理解NovaLang语言设计

**我的指令**：
"详细阅读李圣元2024150118实验一文件夹下内容，理解我设计的NovaLang语言的所有特性。"

**智能体响应**：
全面阅读了实验一的grammar.ebnf（EBNF文法定义）、decisions.md（8项设计决策记录）、scenarios/S1-S6.src（6个场景示例程序）、README.md（构建说明）。

NovaLang核心特性总结：
- 缩进块结构（Python风格，冒号+缩进）
- 强制@类型注解（使用变量时必加@类型）
- 禁止C风格强转，统一通过对象方法toFloat()/toInt()
- 函数定义`fn(返回类型) 函数名 -> 参数列表:`
- 函数调用`函数名->(参数列表)`
- 数组双形态：声明`int a[5]`、元素访问`a[0]@int`、整体引用`a@int[5]`
- 运算符体系沿用C++
- 程序入口：`fn(void) main ->:`

**工作纪要**：
- 决策：确定类型系统的核心规则——严格类型匹配、显式转换、@类型注解验证
- 决策理由：NovaLang的设计哲学是"类型透明"，所有转换和类型信息对读者可见
- 验证：对照grammar.ebnf确认了所有语法结构的类型语义

---

## 第三轮：设计符号表数据结构

**我的指令**：
"基于NovaLang的语言特性，设计嵌套作用域符号表的数据结构。需要考虑：三级作用域（global→function→block）、变量遮蔽、前向引用。"

**智能体响应**：
设计了作用域栈（Scope Stack）结构：
- Symbol类：记录name, sym_type, kind, line, col, scope_level, params, return_type, array_size
- Scope类：单个作用域，维护symbols字典（name→Symbol）和level层级
- SymbolTable类：管理scopes栈，提供enter_scope()/exit_scope()/define()/lookup()/lookup_current_scope()方法
- lookup()从栈顶向栈底搜索，天然支持变量遮蔽
- lookup_current_scope()仅在当前作用域搜索，用于重复声明检测

**工作纪要**：
- 决策：采用作用域栈而非单表+层级标记，因为栈结构更直观且支持嵌套的进入/退出
- 决策理由：递归下降遍历AST时，作用域的进入/退出与AST节点访问天然对应，栈操作简单高效
- 验证：用手工追踪S2场景的三个value变量验证遮蔽逻辑的正确性

---

## 第四轮：实现语义分析器核心

**我的指令**：
"实现semantic_module.py。需要：访问者模式遍历AST、两遍分析（先收集函数声明、再检查函数体）、每种AST节点对应的检查方法、7种语义错误的检测。"

**智能体响应**：
生成了约400行的semantic_module.py，包含完整的SemanticAnalyzer类：
- check()入口：两遍分析策略
- _declare_function()：第一遍注册函数签名
- _check_function()：第二遍检查函数体（进入作用域→声明参数→检查语句→退出作用域）
- _check_statement()：语句分发（VarDecl, AssignStmt, IfStmt, WhileStmt, ReturnStmt, ExprStmt, BreakStmt, ContinueStmt）
- _check_expr()：表达式类型推导（返回类型字符串）
- _check_binary_expr()：运算符类型检查（分类处理算术/关系/相等/逻辑运算）
- _check_call_expr()：函数调用检查（参数个数+类型）
- _check_method_call()：方法调用检查（toFloat/toInt）
- _check_typed_var_ref()：@类型注解验证

**工作纪要**：
- 决策：所有表达式检查方法返回类型字符串，使得类型信息可以从叶子向上传播
- 决策理由：这种"递归类型推导"模式天然适合表达式树的自底向上分析
- 决策：发现错误后不中断，继续分析。调用self.error()记录而非抛出异常
- 验证：对S1-S5场景运行check命令，S1-S5全部0 errors，S6正确返回词法+语法错误

---

## 第五轮：解决print内置函数问题

**我的指令**：
"所有场景都用了print->()但没有声明print函数，导致UNDECLARED错误。需要处理这个问题。"

**智能体响应**：
建议添加_register_builtins()方法，在全局作用域初始化时注册print等内置函数。print参数类型设为"any"以接受任意类型实参，并在参数类型检查中对"any"做特殊处理（跳过检查）。

**工作纪要**：
- 决策：采用内置函数注册机制而非修改语法规则
- 决策理由：内置函数是编译器标准做法（如C的printf、Python的print），避免污染用户代码的符号表
- 验证：重新运行S1-S5，print调用不再报告UNDECLARED错误

---

## 第六轮：编写测试用例

**我的指令**：
"创建10个测试用例，覆盖T1~T5全部场景。每个测试需要.src源文件和.expected.json预期输出。"

**智能体响应**：
生成了10个测试用例：
- test_01_nested_scope.src（T1-1：嵌套作用域）
- test_02_shadow.src（T1-2：变量遮蔽）
- test_03_undeclared.src（T2-1：未声明变量）
- test_04_redeclared.src（T2-2：重复声明）
- test_05_type_mismatch.src（T3-1：类型不匹配）
- test_06_operator_type.src（T3-2：运算符类型错误）
- test_07_arg_count.src（T4-1：参数个数错误）
- test_08_arg_type.src（T4-2：参数类型错误）
- test_09_correct1.src（T5-1：正确程序）
- test_10_correct2.src（T5-2：正确程序+类型转换）

并生成了对应的.expected.json预期输出文件。

**工作纪要**：
- 决策：遵循实验三的测试命名和组织方式（test_NN_description.src + .expected.json）
- 决策理由：保持与前序实验一致的测试结构，便于批量验证
- 验证：运行所有测试，对比实际输出与.expected.json，全部一致

---

## 第七轮：创建S8语义错误场景

**我的指令**：
"创建S8场景——词法语法均正确但包含语义错误的程序。需要在一个文件中覆盖全部7种语义错误类型。"

**智能体响应**：
创建了scenarios/S8.src，包含8个测试函数，每个触发一种语义错误：
1. testUndeclared → UNDECLARED（使用未声明的y）
2. testRedeclared → REDECLARED（重复声明x）
3. testTypeMismatch → TYPE_MISMATCH（string赋值给int）
4. testReturnMismatch → RETURN_TYPE_MISMATCH（返回string但声明int）
5. testArgCount → ARG_COUNT_MISMATCH（add需要2参数给1个）
6. testArgType → ARG_TYPE_MISMATCH（string传给int参数）
7. testNotFunc → NOT_A_FUNCTION（变量x当作函数调用）
8. testOpType → TYPE_MISMATCH（int+bool运算）

main函数统一调用所有测试函数。

**工作纪要**：
- 决策：在一份S8文件中覆盖全部错误类型
- 决策理由：便于演示"一次分析报告多个错误"的功能特性
- 验证：运行check命令，确认检测到8个错误，覆盖7种类型

---

## 第八轮：实现选做任务——auto类型推导

**我的指令**：
"选做内容也需要完成。实现auto关键字的局部变量类型推导功能。"

**智能体响应**：
完成了三层修改：
1. 词法层：KEYWORD正则添加auto
2. 语法层：is_stmt_start添加auto识别、新增parse_auto_decl()方法（解析`auto name = expr`）、parse_statement添加auto分发
3. 语义层：_check_statement添加AutoVarDecl分发、新增_check_auto_decl()方法（从初始化表达式推导类型）

创建test_11_auto_infer.src测试用例，验证auto推导int/float/bool类型。

**工作纪要**：
- 决策：选择实现auto类型推导而非复杂类型扩展
- 决策理由：auto关键字与NovaLang"减少语法噪声"的设计哲学一致，实现复杂度适中
- 验证：运行check命令，auto声明的变量被正确推导（5→int, 3.14→float, true→bool），使用@类型注解验证通过

---

## 第九轮：生成docx格式实验报告

**我的指令**：
"实验报告需要docx格式，内容必须完整覆盖题目要求的三个方面：(1)完整功能演示流程（图文并茂）；(2)设计与实现说明（5个子问题）；(3)AI协作过程小结。报告风格需要匹配前序实验报告。"

**智能体响应**：
编写了generate_report.py脚本，使用python-docx库生成格式化的docx报告，包含：
- 封面（标题、姓名、学号、日期）
- 八章正文：实验概述、实验目标、设计与实现说明、完整功能演示流程、AI协作过程小结、问题与解决、总结、交付物清单
- 中文字体设置（宋体正文、黑体标题、Consolas代码）
- 页边距和段落格式
- 表格（类型系统表、错误类型表、测试结果表）
- 代码块和JSON输出块（含实际check运行结果）

**工作纪要**：
- 决策：使用python-docx脚本自动生成而非手动编写Word文档
- 决策理由：可以嵌入实际的check命令输出结果，确保报告中演示的输出与代码实际行为一致
- 验证：生成的docx文件已确认存在（51KB），内容覆盖所有必选章节

---

## 第十轮：报告内容增强——详细代码讲解

**我的指令**：
"实验报告内容步骤需要详细讲解代码思路以及对应的代码块。"

**智能体响应**：
重写了generate_report.py，在第三章节（设计与实现说明）中大幅增强了代码讲解部分。
新增了14个子章节，每个子章节包含：
1. 设计思路的文字说明
2. 从semantic_module.py中提取的完整代码块
3. 代码逻辑的逐行解析

具体覆盖内容：
- 3.1 整体架构与工作流程（含check命令入口代码）
- 3.2 符号表数据结构（Symbol/Scope/SymbolTable三类完整代码+注释）
- 3.3 两遍分析策略（check()入口方法和两遍遍历代码）
- 3.4 语句检查分发机制（_check_statement路由代码）
- 3.5 变量声明检查（_check_var_decl四步流程代码）
- 3.6 表达式类型推导系统（_check_expr分发+递归推导过程图解）
- 3.7 二元表达式运算符检查（_check_binary_expr分类约束代码）
- 3.8 函数调用检查（_check_call_expr四步流程+any类型处理）
- 3.9 控制流语句作用域管理（_check_if的enter/exit_scope代码）
- 3.10 return语句类型匹配（_check_return代码）
- 3.11 方法调用检查（_check_method_call内置方法代码）
- 3.12 错误检测与恢复策略（SemanticError类+容错机制说明）
- 3.13 auto类型推导完整实现（词法/语法/语义三层代码）
- 3.14 @类型注解交叉验证（_check_typed_var_ref代码）
- 3.15 与前后端实验对接

**工作纪要**：
- 决策：从semantic_module.py提取实际代码块而非手写伪代码，确保报告中的代码与提交的源代码一致
- 验证：生成的docx报告57KB，代码块与源文件内容一致

## 第十一轮：最终全面验证

**我的指令**：
"确认所有功能正常，报告完整。"

**智能体响应**：
运行了全面验证确认：
- S1-S5场景：全部0 errors
- S8场景：8 errors，覆盖7种类型
- 11个测试用例：全部通过
- auto类型推导：正确推导int/float/bool
- docx报告：57KB，含14个子章节的代码讲解
- 对话记录：11轮完整记录

**工作纪要**：
- 最终验证通过，所有交付物齐全
