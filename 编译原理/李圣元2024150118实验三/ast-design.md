# AST节点设计文档

## 一、设计原则

1. **一致性**: 同类结构生成一致的节点形态
2. **完整性**: 每个节点包含type字段标识类型
3. **位置信息**: 每个节点保留line和col字段
4. **可扩展**: 便于后续实验（语义分析、代码生成）复用

## 二、节点定义

### 1. 程序节点 (Program)

```json
{
  "type": "Program",
  "funcs": [<FuncDecl>, ...],
  "line": 1,
  "col": 1
}
```

### 2. 函数声明 (FuncDecl)

```json
{
  "type": "FuncDecl",
  "name": "函数名",
  "return_type": "int|float|string|bool|void",
  "params": [<ParamDecl>, ...],
  "body": [<Statement>, ...],
  "line": 1,
  "col": 1
}
```

### 3. 参数声明 (ParamDecl)

```json
{
  "type": "ParamDecl",
  "name": "参数名",
  "param_type": "int|float|string|bool",
  "array_size": "5",  // 可选，数组参数
  "line": 1,
  "col": 1
}
```

### 4. 变量声明 (VarDecl)

```json
{
  "type": "VarDecl",
  "var_type": "int|float|string|bool",
  "name": "变量名",
  "size": "5",     // 可选，数组大小
  "init": <Expr>,  // 可选，初始值
  "line": 1,
  "col": 1
}
```

### 5. 赋值语句 (AssignStmt)

```json
{
  "type": "AssignStmt",
  "target": <TypedVarRef|TypedArrayElemRef>,
  "value": <Expr>,
  "line": 1,
  "col": 1
}
```

### 6. 条件语句 (IfStmt)

```json
{
  "type": "IfStmt",
  "cond": <Expr>,
  "then": [<Statement>, ...],
  "else": [<Statement>, ...],  // 可选
  "line": 1,
  "col": 1
}
```

### 7. 循环语句 (WhileStmt)

```json
{
  "type": "WhileStmt",
  "cond": <Expr>,
  "body": [<Statement>, ...],
  "line": 1,
  "col": 1
}
```

### 8. 返回语句 (ReturnStmt)

```json
{
  "type": "ReturnStmt",
  "expr": <Expr>,  // 可选
  "line": 1,
  "col": 1
}
```

### 9. 二元表达式 (BinaryExpr)

```json
{
  "type": "BinaryExpr",
  "op": "+|-|*|/|%|==|!=|<|<=|>|>=|&&||",
  "left": <Expr>,
  "right": <Expr>,
  "line": 1,
  "col": 1
}
```

### 10. 一元表达式 (UnaryExpr)

```json
{
  "type": "UnaryExpr",
  "op": "!|-",
  "operand": <Expr>,
  "line": 1,
  "col": 1
}
```

### 11. 函数调用 (CallExpr)

```json
{
  "type": "CallExpr",
  "callee": <Expr>,
  "args": [<Expr>, ...],
  "line": 1,
  "col": 1
}
```

### 12. 标识符 (Identifier)

```json
{
  "type": "Identifier",
  "name": "标识符名",
  "line": 1,
  "col": 1
}
```

### 13. 带类型引用 (TypedVarRef)

```json
{
  "type": "TypedVarRef",
  "name": "变量名",
  "ref_type": "int|float|string|bool",
  "line": 1,
  "col": 1
}
```

### 14. 数组引用 (TypedArrayRef)

```json
{
  "type": "TypedArrayRef",
  "name": "数组名",
  "ref_type": "int|float|string|bool",
  "size": "5",
  "line": 1,
  "col": 1
}
```

### 15. 数组元素引用 (TypedArrayElemRef)

```json
{
  "type": "TypedArrayElemRef",
  "name": "数组名",
  "index": <Expr>,
  "ref_type": "int|float|string|bool",
  "line": 1,
  "col": 1
}
```

### 16. 字面量

- IntLiteral: `{"type": "IntLiteral", "value": "123", "line": 1, "col": 1}`
- FloatLiteral: `{"type": "FloatLiteral", "value": "3.14", "line": 1, "col": 1}`
- StringLiteral: `{"type": "StringLiteral", "value": "\"hello\"", "line": 1, "col": 1}`
- BoolLiteral: `{"type": "BoolLiteral", "value": "true|false", "line": 1, "col": 1}`

## 三、示例

源代码：
```
fn(int) add -> a@int, b@int:
    return a@int + b@int
```

AST：
```json
{
  "type": "Program",
  "funcs": [
    {
      "type": "FuncDecl",
      "name": "add",
      "return_type": "int",
      "params": [
        {"type": "ParamDecl", "name": "a", "param_type": "int", "line": 1, "col": 16},
        {"type": "ParamDecl", "name": "b", "param_type": "int", "line": 1, "col": 25}
      ],
      "body": [
        {
          "type": "ReturnStmt",
          "expr": {
            "type": "BinaryExpr",
            "op": "+",
            "left": {"type": "TypedVarRef", "name": "a", "ref_type": "int", "line": 2, "col": 12},
            "right": {"type": "TypedVarRef", "name": "b", "ref_type": "int", "line": 2, "col": 20},
            "line": 2,
            "col": 12
          },
          "line": 2,
          "col": 5
        }
      ],
      "line": 1,
      "col": 1
    }
  ],
  "line": 1,
  "col": 1
}
```
