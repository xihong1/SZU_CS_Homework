# 实验二：词法分析

## 一、概述

本目录包含了基于实验一所设计的编程语言，实现的手写词法分析器（Scanner）。
分析器以 Python 编写，通过正则表达式最长匹配原则处理输入的源代码文本，生成标准的 Token 序列以及词法错误报告。

## 二、文件结构

- `compiler.py`: 词法分析器核心实现与命令行入口。
- `tests/`: 包含 10 个测试用例 (`.src` 及对应的结果 `.expected.json`)，覆盖所有的测试场景 (T1 - T6)。
- `../scenarios/`: 包含提供的必考场景程序及其生成的 tokenize 结果。

## 三、构建与运行

本实验采用 Python 编写，因此无需特殊的编译过程。确保计算机已安装 Python 3 环境。

### 1. 运行 Tokenize 命令

可以在命令行中使用如下命令将源代码文件转化为 Token JSON 文本：

```bash
python compiler.py tokenize <input.src>
```

例如，运行一个测试用例：
```bash
python compiler.py tokenize tests/test_01.src
```

## 四、功能实现说明

- **基本类型识别**：通过预定义的 Token 规范与正则表达式区分 `KEYWORD`, `ID`, `NUM`, `STRING`, `OP`, `DELIM` 等类别。
- **最长匹配**：Python 的正则引擎会按照设定的模式列表顺序，以及对应正则提取引擎中能匹配到的最长字符串进行分析处理（例如 `==` 优先于 `=`）。
- **错误恢复**：
    - 在发生词法错误时（如 `UNCLOSED_STRING` 等），会产生错误并在当前行或标记终止处恢复。
    - 若出现无法识别的字符配置为 `ILLEGAL_CHAR`（如 `$` 符），也会通过单独捕捉错误后，继续分析下一个字符，不会令程序崩溃停止。
- **精确行列信息**：词法分析器按串扫描过程动态更新行和列信息（特别针对包含换行和 `Tab` 的情形严格计算），完全满足实验的追踪需求。

## 五、附加项（任务四）

本项目额外完成了 [正则表达式到 NFA 及 DFA 的自动机构造过程展示]。基于 Thompson 构造法以及子集构造法 (Subset Construction)，将简化的标识符与数字的合成规则转换为图示输出。

运行方式：

```bash
python compiler.py visualize-dfa
```

程序将会输出在控制台：
1. **状态转换矩阵表 (DFA Transition Table)**
2. 一段 **Mermaid 代码**，你可以直接将其复制进 Markdown (如Typora/Github/语雀) 的 `mermaid` 模块里生成可视化的状态流程节点图。

## 六、测试情况

已生成至少 10 个完整的测试场景，分布包含所有要求 T1~T6 场景。
场景 `S1-S6` 也在上级文件夹 `scenarios/` 下正确运行并输出对应 `.tokens.json` 文件供深入参考。