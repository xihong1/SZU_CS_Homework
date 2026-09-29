# 深圳大学实验报告 LaTeX 模板

本项目依据上级目录中的 `实验报告模板.doc` 制作，保留了原模板的五页结构、Letter 纸张、页边距、封面字段和正文外框。

## 使用方法

1. 在 `main.tex` 顶部的“学生信息填写区”填写专业、姓名、学号、班级和日期。
2. 在 `main.tex` 各个注释标出的正文填写区内填写报告内容。
3. 将流程图和运行截图放入 `images` 目录。
4. 使用 XeLaTeX 编译：

   ```bash
   latexmk -xelatex main.tex
   ```

   也可以直接运行 `make`。项目使用 `ctex` 处理中文，建议安装较完整的 TeX Live、MacTeX 或 MiKTeX。

正文内容框会根据内容自动增高；当前页空间不足时会自动续到下一页，后面的部分也会自动向后移动。课程、教师、段落标题等固定模板信息集中在 `template-info.tex` 中。

## 本报告的图、表、代码编号

正文框不是浮动环境（`tcolorbox` + `breakable`），所以图、表、代码都用自定义命令手工编号，
不要再用 `figure` / `table` 浮动环境，否则会出现“浮动体丢失”。

| 命令 | 用法 | 说明 |
| --- | --- | --- |
| `\reportfigure[缩放]{标签}{文件名}{图题}` | `\reportfigure[0.9]{fig:clk}{fig10_clock_tree.png}{系统时钟树}` | 插入 `images/` 下的图片并自动编号，正文用 `\ref{fig:clk}` 引用 |
| `\reportcaption{标签}{表题}` | `\reportcaption{tab:clk}{系统时钟的主要参数}` | 放在 `tabular` 上方，自动编号，正文用 `\ref{tab:clk}` 引用 |
| `\codesrc{代码题注}` | `\codesrc{led.h —— 引脚宏定义}` | 放在 `lstlisting` 上方，自动编号 |

## 配图

`images/` 下的 `fig01` ~ `fig12` 由脚本生成，可以按需要重新出图：

```bash
cd figures
python gen_figures.py      # 需要 Python 3 + matplotlib，中文用微软雅黑
```

* `fig01` ~ `fig10` 是脚本画出来的示意图（框图、流程图、时序图等）。
* `fig11`、`fig12` 是上级目录里 `引脚配置图.png`、`时钟配置图.png` 的副本
  （文件名改成 ASCII，避免 XeLaTeX 处理中文文件名时出问题）。

## 源文件

与报告配套的完整源代码放在上级目录的 `led_test_李圣云_2024150118/` 中，
其中的 `.c` / `.h` 文件是从本报告的代码清单里直接提取的，内容完全一致。
