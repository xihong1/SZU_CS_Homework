# 实验五 AI 协作对话记录

## 第一轮：需求分析
**指令**：阅读实验五PDF要求，理解实验目标和交付物
**响应**：通过pdftotext提取了PDF内容。实验五要求：任务一生成中间代码(TAC/字节码/解释三选一)，任务二实现2-3种优化，任务三IR执行(选做)，任务四场景验证。交付物包括源代码、README、IR设计文档、优化对比、场景IR、对话记录、实验报告。
**决策**：选择三地址码(TAC)作为中间表示——最符合教学要求且便于实现优化
**验证**：列出全部待办事项

## 第二轮：设计IR指令集
**指令**：基于NovaLang语言特性，设计TAC指令集
**决策**：
- 设计了18种操作码，覆盖数据移动(li/mov)、算术(add/sub/mul/div/mod)、比较(lt/le/gt/ge/eq/ne)、逻辑(and_/or_/not_)、跳转(jmp/jz/jnz)、函数(call/param/ret/retv/alloc)、数组(load/store/alloc_array)、转换(toFloat/toInt)、输出(print_)
- 指令内部表示为dict: {"op": "...", "args": [...], "result": "..."}
- 标签使用func_前缀避免名称冲突
**验证**：对照grammar.ebnf确认覆盖所有语法结构

## 第三轮：实现代码生成器
**指令**：实现codegen_module.py核心代码生成器
**决策**：
- TACGen类维护instructions/temp_counter/label_counter
- _gen_expr()采用后序遍历AST递归翻译策略
- _gen_if()/_gen_while()采用标准TAC控制流模式
- _gen_function()生成标签+序言+体+默认返回
- _gen_call()生成param链+call指令
**验证**：对S1场景手工追踪AST到TAC的翻译过程

## 第四轮：实现优化器
**指令**：实现4种优化pass
**决策**：
- 常量折叠：扫描所有二元运算指令，两个操作数均为常量时用eval计算结果替换
- 常量传播：先扫描li/mov建立常量表，然后在其他指令中替换引用
- 代数化简：x*1→x, x+0→x, x*0→0, x/1→x
- 死代码消除：收集used变量集，过滤未被引用的临时变量赋值
- 迭代执行直到收敛（最多5轮）
**验证**：使用test_opt_demo.src生成优化前后对比

## 第五轮：实现IR解释器(选做)
**指令**：实现run命令执行TAC
**决策**：
- 使用完整内存快照(saved_mem)进行函数调用的上下文保存/恢复
- 解释器维护memory/arrays/param_stack/ret_stack/saved_mem
- 从func_main标签开始执行
- 使用_find_func_start跳过函数序言
**验证**：简单add(3,4)→7正确

## 第六轮：修复call标签不匹配
**问题**：函数标签用func_fib但call指令用fib，导致解释器找不到函数
**解决**：在_gen_call中将callee_name加上func_前缀
**验证**：重新运行后跳转正确

## 第七轮：修复alloc指令result字段
**问题**：alloc指令result为None导致变量未正确初始化
**解决**：在emit时显式设置result=var_name
**验证**：变量初始化正确，add函数输出'7'

## 第八轮：生成场景IR和优化对比
**指令**：批量生成S1-S5的IR和优化后IR
**决策**：使用bash循环批量运行codegen命令
**验证**：检查生成的IR文件，确认语法结构翻译正确

## 第九轮：撰写文档
**指令**：生成ir-design.md、README.md、实验报告.md
**决策**：ir-design.md包含完整指令集定义表和控制流翻译模式；报告遵循实验四格式
**验证**：对照题目要求逐项检查文档覆盖度
