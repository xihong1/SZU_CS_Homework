# 实验五：中间代码生成与优化

## 一、概述

在实验四语义分析器的基础上，实现了 NovaLang 编译器的中间代码生成阶段。采用**三地址码 (TAC)** 作为中间表示，支持完整的表达式翻译、控制流翻译和函数调用翻译，并实现了4种代码优化。

## 二、文件结构

```
实验五/
├── compiler.py              # 主编译器 (tokenize/parse/check/codegen/run)
├── codegen_module.py        # 中间代码生成器 + 优化器 + 解释器
├── semantic_module.py       # 语义分析器（来自实验四）
├── ir-design.md             # IR指令集设计文档
├── README.md                # 本文件
├── scenarios/
│   ├── S1.src ~ S5.src      # 场景源文件
│   └── S*.ir.txt / S*.opt.ir.txt  # 优化前后中间代码
├── tests/
│   ├── test_opt_demo.src    # 优化演示用例
│   └── test_opt_demo.*.txt  # 优化前后对比
└── conversation/            # AI协作对话记录
```

## 三、构建与运行

```bash
# 中间代码生成
python compiler.py codegen <input.src>

# 中间代码生成 + 优化
python compiler.py codegen <input.src> --optimize

# IR解释执行（选做）
python compiler.py run <input.src>
python compiler.py run <input.src> --optimize
```

## 四、中间表示选择

选择**三地址码 (TAC)**：
- 每条指令最多三个地址（两个源操作数 + 一个目标）
- 形式统一，接近汇编但独立于机器
- 便于实现数据流分析和代码优化

## 五、实现的优化

| 优化 | 效果 | 示例 |
|------|------|------|
| 常量折叠 | 编译期计算常量表达式 | `2*3` → `6` |
| 常量传播 | 用已知常量替换变量引用 | `t=5; param t` → `param 5` |
| 代数化简 | 利用代数恒等式简化 | `x*1` → `x`, `x+0` → `x` |
| 死代码消除 | 删除未使用的临时变量赋值 | 消除从未被引用的t变量 |

## 六、命令行示例

```bash
# 生成S1的中间代码
python compiler.py codegen scenarios/S1.src

# 对比优化效果
python compiler.py codegen tests/test_opt_demo.src
python compiler.py codegen tests/test_opt_demo.src --optimize
```
