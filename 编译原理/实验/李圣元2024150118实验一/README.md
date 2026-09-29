# 实验一交付 - 文法分析器（任务一 + 任务三）

本项目使用 C++17 实现 `grammar_analyzer`，支持：
- `--check-type`：Chomsky 文法类型判定
- `--validate`：文法合法性验证
- `--stats`：文法统计信息
- `--ambiguity-check --max-length N`：二义性检测（加分项）

## 1. 构建方式（Linux）

```bash
make
```
或将main.cpp编译为可执行文件
```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic -o grammar_analyzer src/main.cpp
```
生成可执行文件：`./grammar_analyzer`

## 2. 运行方式

```bash
./grammar_analyzer input.txt --check-type
./grammar_analyzer input.txt --validate
./grammar_analyzer input.txt --stats
./grammar_analyzer input.txt --ambiguity-check --max-length 8
```

## 3. 输入格式说明

输入文法文件需要包含如下字段：
- `N:` 非终结符集合（空格分隔）
- `T:` 终结符集合（空格分隔）
- `P:` 产生式区块（每行一条，可用 `|` 分隔候选式）
- `START:` 开始符号

支持 `epsilon` 或 `$\\varepsilon$` 表示空串；以 `#` 开头行为注释。

## 4. 主要实现说明

- 文法解析：支持带空格与不带空格的符号串解析。
- 合法性验证：
  - `FORMAT_ERROR`
  - `START_NOT_IN_N`
  - `UNDEFINED_SYMBOL`
  - `UNREACHABLE`
  - `NON_GENERATING`
- 类型判定：按照 3/2/1/0 型优先级输出最严格类型。
- 二义性检测：对长度不超过 `max-length` 的字符串做有界左最推导搜索，若同一终结符串出现至少两条左最推导，输出反例。

## 5. 测试样例

测试文法放在 `tests/` 目录，覆盖：
- 3型（左线性/右线性）
- 2型
- 1型
- 0型
- 非法文法（格式错误、未定义符号、不可达、不可生成等）

## 6. 交付清单对应

- 源代码：`src/main.cpp`
- 构建说明：`README.md`
- 测试集：`tests/`

