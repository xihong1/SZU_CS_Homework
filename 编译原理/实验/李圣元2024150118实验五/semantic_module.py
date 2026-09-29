"""
NovaLang 语义分析器 (Semantic Analyzer)
- 符号表构建与作用域管理
- 类型检查
- 语义错误检测与报告
"""


class Symbol:
    """符号表条目"""
    def __init__(self, name, sym_type, kind, line, col, scope_level,
                 params=None, return_type=None, array_size=None):
        self.name = name
        self.sym_type = sym_type      # 类型字符串
        self.kind = kind               # 'var' | 'param' | 'func' | 'array'
        self.line = line
        self.col = col
        self.scope_level = scope_level
        self.params = params or []     # [(name, type), ...] for functions
        self.return_type = return_type
        self.array_size = array_size   # for array variables

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.sym_type,
            "scope": self._scope_name(),
            "line": self.line,
        }

    def _scope_name(self):
        if self.scope_level == 0:
            return "global"
        elif self.scope_level == 1:
            return "function"
        else:
            return "block"


class Scope:
    """单个作用域"""
    def __init__(self, level=0):
        self.symbols = {}   # name -> Symbol
        self.level = level

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        return self.symbols.get(name)

    def contains(self, name):
        return name in self.symbols


class SymbolTable:
    """嵌套作用域符号表"""
    def __init__(self):
        self.scopes = []        # 作用域栈
        self.all_symbols = []   # 所有已定义符号（用于输出）

    def enter_scope(self):
        level = len(self.scopes)
        self.scopes.append(Scope(level))

    def exit_scope(self):
        if self.scopes:
            self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1] if self.scopes else None

    def current_level(self):
        return len(self.scopes) - 1

    def define(self, symbol):
        """在当前作用域中定义符号"""
        scope = self.current_scope()
        if scope:
            symbol.scope_level = scope.level
            scope.define(symbol)
        self.all_symbols.append(symbol)

    def lookup(self, name):
        """从内到外查找符号"""
        for scope in reversed(self.scopes):
            sym = scope.lookup(name)
            if sym is not None:
                return sym
        return None

    def lookup_current_scope(self, name):
        """仅在当前作用域查找"""
        scope = self.current_scope()
        if scope:
            return scope.lookup(name)
        return None

    def in_global_scope(self):
        return len(self.scopes) <= 1


class SemanticError(Exception):
    """语义错误"""
    def __init__(self, error_type, message, line, col, **extra):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.col = col
        self.extra = extra  # 额外字段如 symbol, expected, found

    def to_dict(self):
        d = {
            "type": self.error_type,
            "line": self.line,
            "col": self.col,
        }
        d.update(self.extra)
        return d


# 类型兼容性规则
VALID_ARITHMETIC_TYPES = {"int", "float"}
VALID_RELATIONAL_TYPES = {"int", "float"}
VALID_LOGICAL_TYPES = {"bool"}
VALID_EQUALITY_TYPES = {"int", "float", "string", "bool"}

# 二元运算符分类
ARITHMETIC_OPS = {"+", "-", "*", "/", "%"}
RELATIONAL_OPS = {"<", "<=", ">", ">="}
EQUALITY_OPS = {"==", "!="}
LOGICAL_OPS = {"&&", "||"}
UNARY_OPS = {"!", "-"}


def is_numeric_type(t):
    return t in ("int", "float")


def is_valid_type(t):
    return t in ("int", "float", "string", "bool", "void")


class SemanticAnalyzer:
    # 内置函数：print 接受任意类型参数，返回 void
    BUILTINS = {
        "print": {"return_type": "void", "params": [("value", "any")], "variadic": False},
    }

    def __init__(self):
        self.symtab = SymbolTable()
        self.errors = []
        self.current_function = None  # 当前分析的函数名/return_type

    def error(self, error_type, message, line, col, **extra):
        err = SemanticError(error_type, message, line, col, **extra)
        self.errors.append(err)

    def _register_builtins(self):
        """注册内置函数到全局作用域"""
        for name, info in self.BUILTINS.items():
            sym = Symbol(name, f"{info['return_type']}({','.join(p[1] for p in info['params'])})",
                         "func", 0, 0, self.symtab.current_level(),
                         params=info["params"], return_type=info["return_type"])
            sym.is_builtin = True
            self.symtab.define(sym)

    def check(self, ast):
        """入口：对整个AST进行语义检查"""
        self.errors = []
        self.symtab = SymbolTable()

        if ast is None:
            return {"errors": [], "symbols": []}

        self.symtab.enter_scope()  # 全局作用域

        # 注册内置函数
        self._register_builtins()

        # 第一遍：收集所有函数声明（以便支持前向引用）
        funcs = ast.get("funcs", [])
        for func in funcs:
            if func.get("type") == "FuncDecl":
                self._declare_function(func)

        # 第二遍：检查每个函数体
        for func in funcs:
            if func.get("type") == "FuncDecl":
                self._check_function(func)

        self.symtab.exit_scope()

        # 输出符号表信息
        symbols_out = []
        for sym in self.symtab.all_symbols:
            symbols_out.append(sym.to_dict())

        return {
            "errors": [e.to_dict() for e in self.errors],
            "symbols": symbols_out,
        }

    # ============ 声明 ============

    def _declare_function(self, node):
        """第一遍：声明函数签名"""
        name = node.get("name", "")
        return_type = node.get("return_type", "void")
        params = []
        for p in node.get("params", []):
            ptype = p.get("param_type", "int")
            pname = p.get("name", "")
            array_size = p.get("array_size")
            if array_size:
                params.append((pname, f"{ptype}[{array_size}]"))
            else:
                params.append((pname, ptype))

        # 检查重复声明
        existing = self.symtab.lookup_current_scope(name)
        if existing:
            self.error("REDECLARED",
                       f"function '{name}' is already declared",
                       node.get("line", 0), node.get("col", 0),
                       symbol=name)
            return

        # 构建函数类型字符串
        param_types = ",".join(p[1] for p in params)
        func_type = f"{return_type}({param_types})"

        sym = Symbol(name, func_type, "func",
                     node.get("line", 0), node.get("col", 0),
                     self.symtab.current_level(),
                     params=params, return_type=return_type)
        self.symtab.define(sym)

    def _check_function(self, node):
        """第二遍：检查函数体"""
        name = node.get("name", "")
        return_type = node.get("return_type", "void")
        params = node.get("params", [])
        body = node.get("body", [])
        line = node.get("line", 0)
        col = node.get("col", 0)

        # 需要检查 main 函数签名
        if name == "main":
            if return_type != "void" or len(params) != 0:
                # 不强制报错，仅作提醒（按语言设计规范应如此）
                pass

        # 进入函数作用域
        self.symtab.enter_scope()
        self.current_function = {"name": name, "return_type": return_type}

        # 声明参数
        for p in params:
            ptype = p.get("param_type", "int")
            pname = p.get("name", "")
            array_size = p.get("array_size")
            pline = p.get("line", line)
            pcol = p.get("col", col)

            if array_size:
                sym_type = f"{ptype}[{array_size}]"
                sym = Symbol(pname, sym_type, "array",
                             pline, pcol, self.symtab.current_level(),
                             array_size=array_size)
            else:
                sym = Symbol(pname, ptype, "param",
                             pline, pcol, self.symtab.current_level())
            self.symtab.define(sym)

        # 检查函数体语句
        self._check_statement_list(body)

        self.symtab.exit_scope()
        self.current_function = None

    # ============ 语句检查 ============

    def _check_statement_list(self, stmts):
        """检查语句列表"""
        if not stmts:
            return
        for stmt in stmts:
            self._check_statement(stmt)

    def _check_statement(self, node):
        """分发到具体的语句检查方法"""
        if node is None:
            return
        node_type = node.get("type", "")

        if node_type == "VarDecl":
            self._check_var_decl(node)
        elif node_type == "AutoVarDecl":
            self._check_auto_decl(node)
        elif node_type == "AssignStmt":
            self._check_assign(node)
        elif node_type == "IfStmt":
            self._check_if(node)
        elif node_type == "WhileStmt":
            self._check_while(node)
        elif node_type == "ReturnStmt":
            self._check_return(node)
        elif node_type == "ExprStmt":
            self._check_expr(node.get("expr"))
        elif node_type == "BreakStmt":
            pass  # 无类型检查
        elif node_type == "ContinueStmt":
            pass  # 无类型检查
        elif node_type == "Block":
            self._check_statement_list(node.get("body", []))

    def _check_var_decl(self, node):
        """检查变量声明"""
        var_type = node.get("var_type", "int")
        name = node.get("name", "")
        line = node.get("line", 0)
        col = node.get("col", 0)
        init = node.get("init")
        size = node.get("size")

        if not is_valid_type(var_type):
            self.error("TYPE_MISMATCH",
                       f"unknown type '{var_type}'",
                       line, col, expected="valid type", found=var_type)
            var_type = "int"  # 容错

        # 检查重复声明
        existing = self.symtab.lookup_current_scope(name)
        if existing:
            self.error("REDECLARED",
                       f"'{name}' is already declared in this scope",
                       line, col, symbol=name)
            return

        # 声明符号
        if size is not None:
            sym_type = f"{var_type}[{size}]"
            sym = Symbol(name, sym_type, "array",
                         line, col, self.symtab.current_level(),
                         array_size=size)
        else:
            sym = Symbol(name, var_type, "var",
                         line, col, self.symtab.current_level())
        self.symtab.define(sym)

        # 检查初始化表达式
        if init is not None:
            init_type = self._check_expr(init)
            if init_type is not None and init_type != var_type:
                self.error("TYPE_MISMATCH",
                           f"cannot assign '{init_type}' to variable of type '{var_type}'",
                           line, col, expected=var_type, found=init_type)

    def _check_auto_decl(self, node):
        """检查 auto 类型推导声明: auto name = expr
        根据初始化表达式推断变量类型"""
        name = node.get("name", "")
        init = node.get("init")
        line = node.get("line", 0)
        col = node.get("col", 0)

        # 检查重复声明
        existing = self.symtab.lookup_current_scope(name)
        if existing:
            self.error("REDECLARED",
                       f"'{name}' is already declared in this scope",
                       line, col, symbol=name)
            return

        # 推导初始化表达式的类型
        inferred_type = self._check_expr(init)
        if inferred_type is None:
            inferred_type = "int"  # 容错默认

        if not is_valid_type(inferred_type) and not inferred_type.startswith("int[") and not inferred_type.startswith("float[") and not inferred_type.startswith("string[") and not inferred_type.startswith("bool["):
            self.error("TYPE_MISMATCH",
                       f"cannot infer type from expression of type '{inferred_type}'",
                       line, col, expected="valid type", found=inferred_type)
            inferred_type = "int"

        # 声明推导出的类型
        sym = Symbol(name, inferred_type, "var",
                     line, col, self.symtab.current_level())
        self.symtab.define(sym)

    def _check_assign(self, node):
        """检查赋值语句"""
        target = node.get("target", {})
        value = node.get("value")
        line = node.get("line", 0)
        col = node.get("col", 0)

        # 检查左值类型
        target_type = self._check_expr(target)

        # 检查右值类型
        value_type = self._check_expr(value)

        # 类型匹配检查
        if target_type is not None and value_type is not None:
            if target_type != value_type:
                self.error("TYPE_MISMATCH",
                           f"cannot assign '{value_type}' to '{target_type}'",
                           line, col, expected=target_type, found=value_type)

    def _check_if(self, node):
        """检查if语句"""
        cond = node.get("cond", {})
        then_body = node.get("then", [])
        else_body = node.get("else")

        # 检查条件表达式类型
        cond_type = self._check_expr(cond)
        if cond_type is not None and cond_type != "bool":
            self.error("TYPE_MISMATCH",
                       f"if condition must be 'bool', got '{cond_type}'",
                       node.get("line", 0), node.get("col", 0),
                       expected="bool", found=cond_type)

        # then 分支在新作用域中
        self.symtab.enter_scope()
        self._check_statement_list(then_body)
        self.symtab.exit_scope()

        # else 分支在新作用域中
        if else_body:
            self.symtab.enter_scope()
            self._check_statement_list(else_body)
            self.symtab.exit_scope()

    def _check_while(self, node):
        """检查while语句"""
        cond = node.get("cond", {})
        body = node.get("body", [])

        # 检查条件表达式类型
        cond_type = self._check_expr(cond)
        if cond_type is not None and cond_type != "bool":
            self.error("TYPE_MISMATCH",
                       f"while condition must be 'bool', got '{cond_type}'",
                       node.get("line", 0), node.get("col", 0),
                       expected="bool", found=cond_type)

        # 循环体在新作用域中
        self.symtab.enter_scope()
        self._check_statement_list(body)
        self.symtab.exit_scope()

    def _check_return(self, node):
        """检查return语句"""
        expr = node.get("expr")
        line = node.get("line", 0)
        col = node.get("col", 0)

        expected_type = self.current_function.get("return_type", "void") if self.current_function else "void"

        if expr is None:
            # return; (无表达式)
            if expected_type != "void":
                self.error("RETURN_TYPE_MISMATCH",
                           f"expected return type '{expected_type}', but returning nothing",
                           line, col, expected=expected_type, found="void")
        else:
            expr_type = self._check_expr(expr)
            if expr_type is not None and expected_type != "void":
                if expr_type != expected_type:
                    self.error("RETURN_TYPE_MISMATCH",
                               f"expected return type '{expected_type}', got '{expr_type}'",
                               line, col, expected=expected_type, found=expr_type)

    # ============ 表达式检查 ============

    def _check_expr(self, node):
        """检查表达式，返回表达式的类型字符串；出错返回None"""
        if node is None:
            return None

        node_type = node.get("type", "")

        if node_type == "IntLiteral":
            return "int"
        elif node_type == "FloatLiteral":
            return "float"
        elif node_type == "StringLiteral":
            return "string"
        elif node_type == "BoolLiteral":
            return "bool"
        elif node_type == "Identifier":
            return self._check_identifier(node)
        elif node_type == "TypedVarRef":
            return self._check_typed_var_ref(node)
        elif node_type == "TypedArrayRef":
            return self._check_typed_array_ref(node)
        elif node_type == "TypedArrayElemRef":
            return self._check_typed_array_elem_ref(node)
        elif node_type == "BinaryExpr":
            return self._check_binary_expr(node)
        elif node_type == "UnaryExpr":
            return self._check_unary_expr(node)
        elif node_type == "CallExpr":
            return self._check_call_expr(node)
        elif node_type == "MethodCall":
            return self._check_method_call(node)
        elif node_type == "MemberAccess":
            return self._check_member_access(node)
        else:
            return None

    def _check_identifier(self, node):
        """检查标识符引用"""
        name = node.get("name", "")
        line = node.get("line", 0)
        col = node.get("col", 0)

        sym = self.symtab.lookup(name)
        if sym is None:
            self.error("UNDECLARED",
                       f"'{name}' is not declared",
                       line, col, symbol=name)
            return None
        return sym.sym_type

    def _check_typed_var_ref(self, node):
        """检查带类型引用，如 a@int"""
        name = node.get("name", "")
        ref_type = node.get("ref_type", "")
        line = node.get("line", 0)
        col = node.get("col", 0)

        sym = self.symtab.lookup(name)
        if sym is None:
            self.error("UNDECLARED",
                       f"'{name}' is not declared",
                       line, col, symbol=name)
            return ref_type  # 返回标注类型作为容错

        if sym.kind == "func":
            self.error("TYPE_MISMATCH",
                       f"'{name}' is a function, cannot be used as a variable",
                       line, col, expected="variable", found="function")
            return ref_type

        # 类型注解必须与声明类型一致
        declared_type = sym.sym_type
        if declared_type != ref_type:
            self.error("TYPE_MISMATCH",
                       f"'{name}' is declared as '{declared_type}', but used as '{ref_type}'",
                       line, col, expected=declared_type, found=ref_type)

        return ref_type

    def _check_typed_array_ref(self, node):
        """检查数组整体引用，如 a@int[5]"""
        name = node.get("name", "")
        ref_type = node.get("ref_type", "")
        size = node.get("size", "")
        line = node.get("line", 0)
        col = node.get("col", 0)

        sym = self.symtab.lookup(name)
        if sym is None:
            self.error("UNDECLARED",
                       f"'{name}' is not declared",
                       line, col, symbol=name)
            return f"{ref_type}[{size}]"

        if sym.kind != "array":
            self.error("TYPE_MISMATCH",
                       f"'{name}' is not an array",
                       line, col, expected="array", found=sym.kind)
            return f"{ref_type}[{size}]"

        # 检查数组元素类型和大小
        declared_size = sym.array_size
        expected_full_type = f"{ref_type}[{size}]"
        if sym.sym_type != expected_full_type:
            self.error("TYPE_MISMATCH",
                       f"array '{name}' type mismatch: declared '{sym.sym_type}', used as '{expected_full_type}'",
                       line, col, expected=sym.sym_type, found=expected_full_type)

        return expected_full_type

    def _check_typed_array_elem_ref(self, node):
        """检查数组元素引用，如 a[0]@int"""
        name = node.get("name", "")
        index = node.get("index")
        ref_type = node.get("ref_type", "")
        line = node.get("line", 0)
        col = node.get("col", 0)

        sym = self.symtab.lookup(name)
        if sym is None:
            self.error("UNDECLARED",
                       f"'{name}' is not declared",
                       line, col, symbol=name)
            return ref_type

        if sym.kind != "array":
            self.error("TYPE_MISMATCH",
                       f"'{name}' is not an array",
                       line, col, expected="array", found=sym.kind)
            return ref_type

        # 检查元素类型
        # 声明类型如 "int[5]"，元素类型应为 "int"
        declared_elem_type = sym.sym_type.split("[")[0] if "[" in sym.sym_type else sym.sym_type
        if declared_elem_type != ref_type:
            self.error("TYPE_MISMATCH",
                       f"array element type mismatch: declared '{declared_elem_type}', used as '{ref_type}'",
                       line, col, expected=declared_elem_type, found=ref_type)

        # 检查索引表达式类型（应为 int）
        if index:
            idx_type = self._check_expr(index)
            if idx_type is not None and idx_type != "int":
                self.error("TYPE_MISMATCH",
                           f"array index must be 'int', got '{idx_type}'",
                           line, col, expected="int", found=idx_type)

        return ref_type

    def _check_binary_expr(self, node):
        """检查二元表达式"""
        op = node.get("op", "")
        left = node.get("left")
        right = node.get("right")
        line = node.get("line", 0)
        col = node.get("col", 0)

        left_type = self._check_expr(left)
        right_type = self._check_expr(right)

        if left_type is None or right_type is None:
            return None

        # 检查左右类型一致
        if left_type != right_type:
            self.error("TYPE_MISMATCH",
                       f"operator '{op}' requires operands of same type, got '{left_type}' and '{right_type}'",
                       line, col, expected=left_type, found=right_type)
            return left_type  # 容错：返回左类型

        # 按运算符类别检查类型合法性
        if op in ARITHMETIC_OPS:
            if left_type not in VALID_ARITHMETIC_TYPES:
                self.error("TYPE_MISMATCH",
                           f"arithmetic operator '{op}' requires numeric type, got '{left_type}'",
                           line, col, expected="int or float", found=left_type)
            # % 运算符仅对 int 有效
            if op == "%" and left_type != "int":
                self.error("TYPE_MISMATCH",
                           f"modulo operator '%' requires 'int', got '{left_type}'",
                           line, col, expected="int", found=left_type)
            return left_type

        elif op in RELATIONAL_OPS:
            if left_type not in VALID_RELATIONAL_TYPES:
                self.error("TYPE_MISMATCH",
                           f"comparison operator '{op}' requires numeric type, got '{left_type}'",
                           line, col, expected="int or float", found=left_type)
            return "bool"

        elif op in EQUALITY_OPS:
            return "bool"

        elif op in LOGICAL_OPS:
            if left_type != "bool":
                self.error("TYPE_MISMATCH",
                           f"logical operator '{op}' requires 'bool', got '{left_type}'",
                           line, col, expected="bool", found=left_type)
            return "bool"

        return left_type

    def _check_unary_expr(self, node):
        """检查一元表达式"""
        op = node.get("op", "")
        operand = node.get("operand")
        line = node.get("line", 0)
        col = node.get("col", 0)

        operand_type = self._check_expr(operand)
        if operand_type is None:
            return None

        if op == "!":
            if operand_type != "bool":
                self.error("TYPE_MISMATCH",
                           f"logical NOT '!' requires 'bool', got '{operand_type}'",
                           line, col, expected="bool", found=operand_type)
            return "bool"
        elif op == "-":
            if operand_type not in VALID_ARITHMETIC_TYPES:
                self.error("TYPE_MISMATCH",
                           f"unary minus '-' requires numeric type, got '{operand_type}'",
                           line, col, expected="int or float", found=operand_type)
            return operand_type

        return operand_type

    def _check_call_expr(self, node):
        """检查函数调用，如 func->(args)"""
        callee = node.get("callee", {})
        args = node.get("args", [])
        line = node.get("line", 0)
        col = node.get("col", 0)

        # 获取被调用者信息
        callee_type = self._check_expr(callee)

        # 被调用者应该是标识符
        callee_name = callee.get("name", "") if callee else ""
        if not callee_name:
            return None

        sym = self.symtab.lookup(callee_name)
        if sym is None:
            self.error("UNDECLARED",
                       f"function '{callee_name}' is not declared",
                       line, col, symbol=callee_name)
            return None

        if sym.kind != "func":
            self.error("NOT_A_FUNCTION",
                       f"'{callee_name}' is not a function",
                       line, col, symbol=callee_name)
            return None

        # 检查参数个数
        expected_params = sym.params
        if len(args) != len(expected_params):
            self.error("ARG_COUNT_MISMATCH",
                       f"function '{callee_name}' expects {len(expected_params)} arguments, got {len(args)}",
                       line, col, symbol=callee_name,
                       expected=str(len(expected_params)), found=str(len(args)))

        # 检查参数类型
        for i, arg in enumerate(args):
            arg_type = self._check_expr(arg)
            if arg_type is not None and i < len(expected_params):
                expected_type = expected_params[i][1]
                # "any" 类型接受任意参数（用于内置函数如 print）
                if expected_type == "any":
                    continue
                if arg_type != expected_type:
                    self.error("ARG_TYPE_MISMATCH",
                               f"argument {i+1} of '{callee_name}' expects '{expected_type}', got '{arg_type}'",
                               line, col, symbol=callee_name,
                               expected=expected_type, found=arg_type)

        return sym.return_type

    def _check_method_call(self, node):
        """检查方法调用，如 x@int.toFloat()"""
        obj = node.get("object")
        method = node.get("method", "")
        args = node.get("args", [])
        line = node.get("line", 0)
        col = node.get("col", 0)

        obj_type = self._check_expr(obj)

        # NovaLang 内置方法
        if method == "toFloat":
            if obj_type is not None and obj_type != "int":
                self.error("TYPE_MISMATCH",
                           f"'toFloat()' can only be called on 'int', got '{obj_type}'",
                           line, col, expected="int", found=obj_type)
            return "float"

        elif method == "toInt":
            if obj_type is not None and obj_type != "float":
                self.error("TYPE_MISMATCH",
                           f"'toInt()' can only be called on 'float', got '{obj_type}'",
                           line, col, expected="float", found=obj_type)
            return "int"

        else:
            self.error("UNDECLARED",
                       f"unknown method '{method}'",
                       line, col, symbol=method)
            return None

    def _check_member_access(self, node):
        """检查成员访问，如 x.name"""
        obj = node.get("object")
        member = node.get("member", "")
        line = node.get("line", 0)
        col = node.get("col", 0)

        obj_type = self._check_expr(obj)

        # NovaLang暂时没有结构体成员，记录错误
        self.error("UNDECLARED",
                   f"cannot access member '{member}' on '{obj_type}'",
                   line, col, symbol=member)
        return None


def semantic_check(ast):
    """便捷入口：对AST进行语义检查"""
    analyzer = SemanticAnalyzer()
    return analyzer.check(ast)
