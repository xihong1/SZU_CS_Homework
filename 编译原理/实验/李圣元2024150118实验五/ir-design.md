# NovaLang 三地址码 (TAC) 指令集设计文档

## 一、设计选择

选择**三地址码 (Three-Address Code, TAC)** 作为中间表示。理由：
1. 每条指令最多三个操作数（两个源，一个目标），形式统一
2. 接近汇编但独立于具体机器，便于理解和优化
3. 在编译原理教学中最为常用，与《龙书》教材一致
4. 便于实现数据流分析和代码优化

## 二、指令格式

每条指令为 `result = op arg1, arg2` 或 `op arg1` 的形式。内部表示为 dict：
```json
{"op": "操作码", "args": ["arg1", "arg2"], "result": "dest"}
```

## 三、指令集定义

### 3.1 数据移动

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `li` | `t1 = literal` | 加载立即数（整型、浮点、布尔） |
| `mov` | `t1 = t2` | 变量/临时变量复制 |

### 3.2 算术运算

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `add` | `t1 = t2 + t3` | 加法（int/float） |
| `sub` | `t1 = t2 - t3` | 减法 |
| `mul` | `t1 = t2 * t3` | 乘法 |
| `div` | `t1 = t2 / t3` | 除法 |
| `mod` | `t1 = t2 % t3` | 取模（仅int） |

### 3.3 比较运算（结果为bool）

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `lt` | `t1 = t2 < t3` | 小于 |
| `le` | `t1 = t2 <= t3` | 小于等于 |
| `gt` | `t1 = t2 > t3` | 大于 |
| `ge` | `t1 = t2 >= t3` | 大于等于 |
| `eq` | `t1 = t2 == t3` | 等于 |
| `ne` | `t1 = t2 != t3` | 不等于 |

### 3.4 逻辑运算

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `and_` | `t1 = t2 && t3` | 逻辑与 |
| `or_` | `t1 = t2 \|\| t3` | 逻辑或 |
| `not_` | `t1 = !t2` | 逻辑非 |

### 3.5 控制流

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `label` | `L1:` | 标签定义 |
| `jmp` | `goto L1` | 无条件跳转 |
| `jz` | `if_false t1 goto L1` | t1为假时跳转 |
| `jnz` | `if t1 goto L1` | t1为真时跳转 |

### 3.6 函数调用

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `enter_func` | `# Function: name (n params)` | 函数序言标记 |
| `alloc` | `alloc name:type` | 局部变量/参数分配 |
| `param` | `param t1` | 传递实参 |
| `call` | `t1 = call f, n` | 调用函数f(n个参数)，结果存入t1 |
| `ret` | `return t1` | 返回（带值） |
| `retv` | `return` | 返回（无值/void） |

### 3.7 数组操作

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `alloc_array` | `alloc name:type[size]` | 数组分配 |
| `load` | `t1 = arr[idx]` | 数组元素读取 |
| `store` | `arr[idx] = t1` | 数组元素写入 |

### 3.8 类型转换与输入输出

| 操作码 | 语法 | 说明 |
|--------|------|------|
| `toFloat` | `t1 = toFloat(t2)` | int转float |
| `toInt` | `t1 = toInt(t2)` | float转int |
| `print_` | `print t1` | 输出到标准输出 |

## 四、控制流翻译约定

### if语句
```
    t1 = condition
    if_false t1 goto L_else
    ... then body ...
    goto L_end
L_else:
    ... else body ...
L_end:
```

### if语句（无else）
```
    t1 = condition
    if_false t1 goto L_end
    ... then body ...
L_end:
```

### while循环
```
L_start:
    t1 = condition
    if_false t1 goto L_end
    ... body ...
    goto L_start
L_end:
```

### 函数调用
```
    param arg1
    param arg2
    t_result = call func_name, 2
```

## 五、临时变量与标签分配

- **临时变量**：按 `t0, t1, t2, ...` 顺序分配，使用全局计数器
- **标签**：按 `endif0, endif1, ...` / `else0, else1, ...` / `while0, while1, ...` 命名
- **函数标签**：使用 `func_<函数名>` 格式
