"""
NovaLang 中间代码生成器 (Code Generator)
- 生成三地址码 (Three-Address Code, TAC)
- 支持控制流翻译、函数调用翻译
- 支持代码优化（常量折叠、常量传播、死代码消除、代数化简）
- 支持IR解释执行（选做）
"""

import json


# ============================================================
# TAC 指令集定义
# ============================================================
# 每条指令为 dict: {"op": 操作码, "args": [...], "result": ...}
#
# 操作码说明:
#   mov    - t1 = t2           (复制)
#   li     - t1 = literal      (加载立即数)
#   add    - t1 = t2 + t3      (加法)
#   sub    - t1 = t2 - t3      (减法)
#   mul    - t1 = t2 * t3      (乘法)
#   div    - t1 = t2 / t3      (除法)
#   mod    - t1 = t2 % t3      (取模)
#   neg    - t1 = -t2          (取负)
#   not_   - t1 = !t2          (逻辑非)
#   lt     - t1 = t2 < t3      (小于)
#   le     - t1 = t2 <= t3     (小于等于)
#   gt     - t1 = t2 > t3      (大于)
#   ge     - t1 = t2 >= t3     (大于等于)
#   eq     - t1 = t2 == t3     (等于)
#   ne     - t1 = t2 != t3     (不等)
#   and_   - t1 = t2 && t3     (逻辑与)  [注: 对TAC简化为按位]
#   or_    - t1 = t2 || t3     (逻辑或)
#   load   - t1 = t2[t3]       (数组读)
#   store  - t1[t2] = t3       (数组写)
#   param  - param t1          (传递参数)
#   call   - t1 = call f, n    (调用函数, n个参数)
#   ret    - return t1         (返回)
#   retv   - return            (空返回)
#   label  - L1:               (标签)
#   jmp    - goto L1           (无条件跳转)
#   jz     - if_false t1 goto L1 (条件跳转-假)
#   jnz    - if t1 goto L1     (条件跳转-真)
#   toFloat- t1 = toFloat(t2)  (int转float)
#   toInt  - t1 = toInt(t2)    (float转int)
#   print_ - print t1          (输出)
# ============================================================


class TACGen:
    """三地址码生成器"""

    def __init__(self):
        self.instructions = []   # [(op, args, result)]
        self.temp_counter = 0
        self.label_counter = 0
        self.current_func = None  # 当前函数名

    def new_temp(self):
        t = f"t{self.temp_counter}"
        self.temp_counter += 1
        return t

    def new_label(self, prefix="L"):
        lbl = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return lbl

    def emit(self, op, args=None, result=None):
        """发射一条TAC指令"""
        if args is None:
            args = []
        self.instructions.append({"op": op, "args": args, "result": result})

    def emit_label(self, label):
        self.emit("label", result=label)

    def generate(self, ast):
        """入口：从AST生成TAC"""
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

        if ast is None:
            return []

        funcs = ast.get("funcs", [])

        # 为每个函数生成代码
        for func in funcs:
            if func.get("type") == "FuncDecl":
                self._gen_function(func)

        return self.instructions

    # ============ 函数 ============

    def _gen_function(self, node):
        name = node.get("name", "")
        params = node.get("params", [])
        body = node.get("body", [])
        self.current_func = name

        # 函数入口标签和序言
        self.emit_label(f"func_{name}")
        self.emit("enter_func", args=[name, str(len(params))])

        # 为参数分配空间（R: param_name:type）
        for p in params:
            ptype = p.get("param_type", "int")
            pname = p.get("name", "")
            array_size = p.get("array_size")
            if array_size:
                self.emit("alloc_array", args=[pname, ptype, str(array_size)], result=pname)
            else:
                self.emit("alloc", args=[pname, ptype], result=pname)

        # 函数体
        self._gen_stmt_list(body)

        # 如果函数体末尾没有return，自动补充默认return
        return_type = node.get("return_type", "void")
        if return_type == "void":
            self.emit("retv")

        self.current_func = None

    # ============ 语句 ============

    def _gen_stmt_list(self, stmts):
        if not stmts:
            return
        for stmt in stmts:
            self._gen_stmt(stmt)

    def _gen_stmt(self, node):
        if node is None:
            return
        t = node.get("type", "")

        if t == "VarDecl":
            self._gen_var_decl(node)
        elif t == "AutoVarDecl":
            self._gen_auto_decl(node)
        elif t == "AssignStmt":
            self._gen_assign(node)
        elif t == "IfStmt":
            self._gen_if(node)
        elif t == "WhileStmt":
            self._gen_while(node)
        elif t == "ReturnStmt":
            self._gen_return(node)
        elif t == "ExprStmt":
            self._gen_expr(node.get("expr"))
        elif t == "BreakStmt":
            # break会由_while处理，这里仅标记
            pass
        elif t == "ContinueStmt":
            pass

    def _gen_var_decl(self, node):
        var_name = node.get("name", "")
        init = node.get("init")
        size = node.get("size")
        var_type = node.get("var_type", "int")

        if size is not None:
            # 数组声明
            self.emit("alloc_array", args=[var_name, var_type, str(size)], result=var_name)
        else:
            # 普通变量声明
            self.emit("alloc", args=[var_name, var_type], result=var_name)

        if init is not None:
            # 有初始化: var_name = init_expr
            result = self._gen_expr(init)
            if result:
                self.emit("mov", args=[result], result=var_name)

    def _gen_auto_decl(self, node):
        var_name = node.get("name", "")
        init = node.get("init")

        if init is not None:
            result = self._gen_expr(init)
            self.emit("alloc", args=[var_name, "auto"], result=var_name)
            if result:
                self.emit("mov", args=[result], result=var_name)

    def _gen_assign(self, node):
        target = node.get("target", {})
        value = node.get("value")

        # 计算右值
        val_result = self._gen_expr(value)

        # 处理左值
        target_type = target.get("type", "")
        if target_type == "TypedVarRef":
            target_name = target.get("name", "")
            if val_result:
                self.emit("mov", args=[val_result], result=target_name)
        elif target_type == "TypedArrayElemRef":
            target_name = target.get("name", "")
            index = target.get("index")
            idx_result = self._gen_expr(index)
            if idx_result and val_result:
                self.emit("store", args=[target_name, idx_result, val_result])

    def _gen_if(self, node):
        cond = node.get("cond", {})
        then_body = node.get("then", [])
        else_body = node.get("else")

        label_else = self.new_label("else")
        label_end = self.new_label("endif")

        # 生成条件代码
        cond_result = self._gen_expr(cond)

        if else_body:
            # if-else: 条件为假跳到else
            if cond_result:
                self.emit("jz", args=[cond_result], result=label_else)
            self._gen_stmt_list(then_body)
            self.emit("jmp", result=label_end)
            self.emit_label(label_else)
            self._gen_stmt_list(else_body)
            self.emit_label(label_end)
        else:
            # if only: 条件为假跳到end
            if cond_result:
                self.emit("jz", args=[cond_result], result=label_end)
            self._gen_stmt_list(then_body)
            self.emit_label(label_end)

    def _gen_while(self, node):
        cond = node.get("cond", {})
        body = node.get("body", [])

        label_start = self.new_label("while")
        label_end = self.new_label("wend")

        self.emit_label(label_start)
        cond_result = self._gen_expr(cond)
        if cond_result:
            self.emit("jz", args=[cond_result], result=label_end)
        self._gen_stmt_list(body)
        self.emit("jmp", result=label_start)
        self.emit_label(label_end)

    def _gen_return(self, node):
        expr = node.get("expr")
        if expr is not None:
            result = self._gen_expr(expr)
            if result:
                self.emit("ret", args=[result])
        else:
            self.emit("retv")

    # ============ 表达式 ============

    def _gen_expr(self, node):
        """生成表达式的TAC代码，返回结果操作数（临时变量名或字面量）"""
        if node is None:
            return None

        t = node.get("type", "")

        # 字面量
        if t == "IntLiteral":
            val = node.get("value", "0")
            tmp = self.new_temp()
            self.emit("li", args=[val], result=tmp)
            return tmp
        elif t == "FloatLiteral":
            val = node.get("value", "0.0")
            tmp = self.new_temp()
            self.emit("li", args=[val], result=tmp)
            return tmp
        elif t == "StringLiteral":
            val = node.get("value", '""')
            tmp = self.new_temp()
            self.emit("li", args=[val], result=tmp)
            return tmp
        elif t == "BoolLiteral":
            val = node.get("value", "false")
            tmp = self.new_temp()
            self.emit("li", args=[val], result=tmp)
            return tmp

        # 标识符/引用
        elif t == "Identifier":
            return node.get("name", "")

        elif t == "TypedVarRef":
            return node.get("name", "")

        elif t == "TypedArrayElemRef":
            name = node.get("name", "")
            index = node.get("index")
            idx_result = self._gen_expr(index)
            tmp = self.new_temp()
            if idx_result:
                self.emit("load", args=[name, idx_result], result=tmp)
            return tmp

        elif t == "TypedArrayRef":
            # 数组整体引用，返回数组名
            return node.get("name", "")

        # 二元表达式
        elif t == "BinaryExpr":
            return self._gen_binary(node)

        # 一元表达式
        elif t == "UnaryExpr":
            return self._gen_unary(node)

        # 函数调用
        elif t == "CallExpr":
            return self._gen_call(node)

        # 方法调用
        elif t == "MethodCall":
            return self._gen_method_call(node)

        return None

    def _gen_binary(self, node):
        op = node.get("op", "")
        left_result = self._gen_expr(node.get("left"))
        right_result = self._gen_expr(node.get("right"))

        if left_result is None or right_result is None:
            return None

        tmp = self.new_temp()

        op_map = {
            "+": "add", "-": "sub", "*": "mul", "/": "div", "%": "mod",
            "<": "lt", "<=": "le", ">": "gt", ">=": "ge",
            "==": "eq", "!=": "ne",
            "&&": "and_", "||": "or_",
        }
        tac_op = op_map.get(op, "add")
        self.emit(tac_op, args=[left_result, right_result], result=tmp)
        return tmp

    def _gen_unary(self, node):
        op = node.get("op", "")
        operand_result = self._gen_expr(node.get("operand"))

        if operand_result is None:
            return None

        tmp = self.new_temp()

        if op == "-":
            self.emit("neg", args=[operand_result], result=tmp)
        elif op == "!":
            self.emit("not_", args=[operand_result], result=tmp)
        return tmp

    def _gen_call(self, node):
        """函数调用: callee->(args)"""
        callee = node.get("callee", {})
        args = node.get("args", [])
        callee_name = callee.get("name", "") if callee else ""

        # 处理内置函数 print
        if callee_name == "print":
            for arg in args:
                arg_result = self._gen_expr(arg)
                if arg_result:
                    self.emit("print_", args=[arg_result])
            return None

        # 传递参数
        for arg in args:
            arg_result = self._gen_expr(arg)
            if arg_result:
                self.emit("param", args=[arg_result])

        # 函数调用 (标签使用 func_ 前缀)
        func_label = f"func_{callee_name}"
        tmp = self.new_temp()
        self.emit("call", args=[func_label, str(len(args))], result=tmp)
        return tmp

    def _gen_method_call(self, node):
        """方法调用: obj.method()"""
        obj = node.get("object")
        method = node.get("method", "")
        obj_result = self._gen_expr(obj)

        tmp = self.new_temp()

        if method == "toFloat":
            if obj_result:
                self.emit("toFloat", args=[obj_result], result=tmp)
            return tmp
        elif method == "toInt":
            if obj_result:
                self.emit("toInt", args=[obj_result], result=tmp)
            return tmp
        return None


# ============================================================
# TAC 优化器
# ============================================================

class TACOptimizer:
    """TAC优化器 — 实现常量折叠、常量传播、死代码消除、代数化简"""

    def __init__(self, instructions):
        self.instructions = list(instructions)  # 深拷贝
        self.const_table = {}  # 已知常量表 varname -> value

    def optimize(self):
        """执行所有优化pass，可重复直到收敛"""
        changed = True
        iteration = 0
        while changed and iteration < 5:
            changed = False
            if self._constant_folding():
                changed = True
            if self._constant_propagation():
                changed = True
            if self._algebraic_simplify():
                changed = True
            iteration += 1
        self._dead_code_elimination()
        return self.instructions

    def _constant_folding(self):
        """常量折叠: 编译期计算常量表达式
        例如: t1 = 2 * 3 → t1 = 6
        """
        changed = False
        for inst in self.instructions:
            op = inst.get("op", "")
            if op in ("add", "sub", "mul", "div", "mod", "lt", "le", "gt", "ge", "eq", "ne", "and_", "or_"):
                args = inst.get("args", [])
                if len(args) == 2:
                    a, b = args[0], args[1]
                    val_a = self._get_const(a)
                    val_b = self._get_const(b)
                    if val_a is not None and val_b is not None:
                        # 两个操作数都是常量，可以折叠
                        try:
                            new_val = self._eval_const(op, val_a, val_b)
                            inst["op"] = "li"
                            inst["args"] = [str(new_val).lower() if isinstance(new_val, bool) else str(new_val)]
                            changed = True
                        except (ValueError, ZeroDivisionError):
                            pass
        return changed

    def _constant_propagation(self):
        """常量传播: 用已知常量替换变量引用
        例如: x = 5; y = x + 1 → y = 6
        注意: 不清除跨函数的常量表，但只传播给临时变量(t开头)，
        避免把main中的 'n=8' 误传播到 fib的参数'n' 上。
        """
        changed = False
        # 首先收集所有常量赋值（仅限临时变量和字面量赋予的变量）
        for inst in self.instructions:
            if inst.get("op") == "li":
                args = inst.get("args", [])
                result = inst.get("result")
                if result and result.startswith("t") and len(args) == 1:
                    try:
                        self.const_table[result] = self._parse_value(args[0])
                    except ValueError:
                        pass
            elif inst.get("op") == "mov":
                args = inst.get("args", [])
                result = inst.get("result")
                # 仅当源是常量且目标是临时变量时才传播
                if result and result.startswith("t") and len(args) == 1 and args[0] in self.const_table:
                    self.const_table[result] = self.const_table[args[0]]
            elif inst.get("op") not in ("label", "jmp", "jz", "jnz", "param", "call",
                                         "print_", "ret", "retv", "enter_func",
                                         "alloc", "alloc_array", "store"):
                # 计算结果的操作使result不再是常量
                result = inst.get("result")
                if result and result in self.const_table:
                    del self.const_table[result]

        # 然后用常量替换变量引用
        for inst in self.instructions:
            op = inst.get("op", "")
            if op in ("add", "sub", "mul", "div", "mod", "lt", "le", "gt", "ge", "eq", "ne", "and_", "or_",
                      "mov", "store", "load", "neg", "not_", "toFloat", "toInt", "print_", "param", "ret"):
                args = inst.get("args", [])
                new_args = []
                for arg in args:
                    if arg in self.const_table:
                        val = self.const_table[arg]
                        new_args.append(str(val).lower() if isinstance(val, bool) else str(val))
                        changed = True
                    else:
                        new_args.append(arg)
                inst["args"] = new_args
        return changed

    def _algebraic_simplify(self):
        """代数化简: x*1→x, x+0→x, x-0→x, x*0→0, x/1→x"""
        changed = False
        for inst in self.instructions:
            op = inst.get("op", "")
            args = inst.get("args", [])
            if len(args) == 2:
                a, b = args[0], args[1]
                va = self._get_const(a)
                vb = self._get_const(b)

                if op == "mul":
                    if vb == 1:
                        # x * 1 → mov x
                        inst["op"] = "mov"; inst["args"] = [a]; changed = True
                    elif va == 1:
                        inst["op"] = "mov"; inst["args"] = [b]; changed = True
                    elif vb == 0 or va == 0:
                        inst["op"] = "li"; inst["args"] = ["0"]; changed = True
                elif op == "add":
                    if vb == 0:
                        inst["op"] = "mov"; inst["args"] = [a]; changed = True
                    elif va == 0:
                        inst["op"] = "mov"; inst["args"] = [b]; changed = True
                elif op == "sub":
                    if vb == 0:
                        inst["op"] = "mov"; inst["args"] = [a]; changed = True
                elif op == "div":
                    if vb == 1:
                        inst["op"] = "mov"; inst["args"] = [a]; changed = True
        return changed

    def _dead_code_elimination(self):
        """死代码消除: 删除从未被使用的临时变量赋值
        扫描所有指令，收集被引用的变量，删除从未被引用的赋值
        """
        # 收集所有被引用的变量
        used = set()
        for inst in self.instructions:
            for arg in inst.get("args", []):
                used.add(arg)
            # 跳转标签也被视为"使用"
            if inst.get("op") in ("jmp", "jz", "jnz"):
                used.add(inst.get("result", ""))

        # 过滤掉未使用的临时变量赋值
        new_insts = []
        for inst in self.instructions:
            op = inst.get("op", "")
            result = inst.get("result", "")

            # 保留非临时变量、跳转、标签、函数调用、store等有副作用的指令
            if op in ("label", "jmp", "jz", "jnz", "param", "call",
                       "print_", "ret", "retv", "enter_func",
                       "alloc", "alloc_array", "store"):
                new_insts.append(inst)
            elif result and result.startswith("t") and result not in used:
                # 临时变量从未被使用，跳过（死代码）
                continue
            elif result and not result.startswith("t"):
                # 非临时变量(用户变量)，保留
                new_insts.append(inst)
            elif not result:
                new_insts.append(inst)
            else:
                # 临时变量被使用了，保留
                new_insts.append(inst)

        self.instructions = new_insts

    def _get_const(self, operand):
        """尝试获取操作数的常量值，若非数字则返回None"""
        try:
            if operand in self.const_table:
                return self.const_table[operand]
            # 布尔字面量
            if operand == "true":
                return True
            if operand == "false":
                return False
            # 浮点数
            if "." in str(operand):
                return float(operand)
            # 整数
            return int(operand)
        except (ValueError, TypeError):
            return None

    def _parse_value(self, s):
        """解析字符串为Python值"""
        if s == "true":
            return True
        if s == "false":
            return False
        try:
            if "." in str(s):
                return float(s)
            return int(s)
        except (ValueError, TypeError):
            return s

    def _eval_const(self, op, a, b):
        """计算常量表达式"""
        if op == "add": return a + b
        if op == "sub": return a - b
        if op == "mul": return a * b
        if op == "div":
            if isinstance(a, int) and isinstance(b, int):
                return a // b  # 整数除法
            return a / b
        if op == "mod": return a % b
        if op == "lt": return a < b
        if op == "le": return a <= b
        if op == "gt": return a > b
        if op == "ge": return a >= b
        if op == "eq": return a == b
        if op == "ne": return a != b
        if op == "and_": return bool(a) and bool(b)
        if op == "or_": return bool(a) or bool(b)
        raise ValueError(f"Unknown op: {op}")


# ============================================================
# TAC 格式化输出
# ============================================================

def format_tac(instructions):
    """将TAC指令列表格式化为可读文本"""
    lines = []
    for inst in instructions:
        op = inst.get("op", "?")
        args = inst.get("args", [])
        result = inst.get("result", "")

        if op == "label":
            lines.append(f"{result}:")
        elif op == "li":
            lines.append(f"    {result} = {args[0]}")
        elif op == "mov":
            lines.append(f"    {result} = {args[0]}")
        elif op in ("neg", "not_", "toFloat", "toInt"):
            op_name = {"neg": "-", "not_": "!", "toFloat": "toFloat", "toInt": "toInt"}
            lines.append(f"    {result} = {op_name.get(op, op)}({args[0]})")
        elif op == "param":
            lines.append(f"    param {args[0]}")
        elif op == "call":
            lines.append(f"    {result} = call {args[0]}, {args[1]}")
        elif op == "ret":
            lines.append(f"    return {args[0]}")
        elif op == "retv":
            lines.append(f"    return")
        elif op == "jmp":
            lines.append(f"    goto {result}")
        elif op == "jz":
            lines.append(f"    if_false {args[0]} goto {result}")
        elif op == "jnz":
            lines.append(f"    if {args[0]} goto {result}")
        elif op == "alloc":
            lines.append(f"    alloc {args[0]}:{args[1]}")
        elif op == "alloc_array":
            lines.append(f"    alloc {args[0]}:{args[1]}[{args[2]}]")
        elif op == "load":
            lines.append(f"    {result} = {args[0]}[{args[1]}]")
        elif op == "store":
            lines.append(f"    {args[0]}[{args[1]}] = {args[2]}")
        elif op == "enter_func":
            lines.append(f"# --- Function: {args[0]} ({args[1]} params) ---")
        elif op == "print_":
            lines.append(f"    print {args[0]}")
        elif op in ("add", "sub", "mul", "div", "mod", "lt", "le", "gt", "ge", "eq", "ne", "and_", "or_"):
            op_sym = {"add": "+", "sub": "-", "mul": "*", "div": "/", "mod": "%",
                       "lt": "<", "le": "<=", "gt": ">", "ge": ">=",
                       "eq": "==", "ne": "!=", "and_": "&&", "or_": "||"}
            lines.append(f"    {result} = {args[0]} {op_sym.get(op, op)} {args[1]}")
        else:
            if result:
                lines.append(f"    {result} = {op}({', '.join(args)})")
            else:
                lines.append(f"    {op}({', '.join(args)})")
    return "\n".join(lines)


def format_tac_json(instructions):
    """将TAC指令列表格式化为JSON"""
    return json.dumps(instructions, ensure_ascii=False, indent=2)


# ============================================================
# TAC 解释器 (选做 — IR执行)
# ============================================================

class TACInterpreter:
    """TAC解释器/虚拟机 — 执行中间代码并输出结果"""

    def __init__(self, instructions):
        self.instructions = instructions
        self.memory = {}       # 变量名 -> 值
        self.arrays = {}       # 数组名 -> [值列表]
        self.labels = {}       # 标签名 -> 指令索引
        self.output = []       # print输出收集
        self.param_stack = []  # 参数传递栈
        self.ret_stack = []    # 返回地址栈
        self.saved_mem = []    # 保存的内存上下文栈（用于函数调用）
        self.ip = 0            # 指令指针

        # 第一遍：建立标签表
        for i, inst in enumerate(instructions):
            if inst.get("op") == "label":
                self.labels[inst.get("result", "")] = i

    def run(self):
        """执行TAC程序，返回输出列表"""
        self.ip = 0
        self.output = []
        self.memory = {}
        self.param_stack = []  # ★ 修复: 这里原来错误地写了 call_stack
        self.ret_stack = []
        self.saved_mem = []

        # 找到main函数的入口
        main_label = "func_main"
        if main_label in self.labels:
            self.ip = self.labels[main_label] + 1  # 跳过标签本身

        while self.ip < len(self.instructions):
            inst = self.instructions[self.ip]
            op = inst.get("op", "")
            args = inst.get("args", [])
            result = inst.get("result", "")

            if op == "label":
                pass
            elif op == "enter_func":
                pass
            elif op == "li":
                self.memory[result] = self._parse_val(args[0]) if args else 0
            elif op == "mov":
                self.memory[result] = self._get_val(args[0]) if args else 0
            elif op in ("add", "sub", "mul", "div", "mod"):
                self.memory[result] = self._arith(op, args)
            elif op in ("lt", "le", "gt", "ge", "eq", "ne"):
                self.memory[result] = self._cmp(op, args)
            elif op in ("and_", "or_"):
                self.memory[result] = self._logic(op, args)
            elif op == "neg":
                self.memory[result] = -self._get_val(args[0])
            elif op == "not_":
                self.memory[result] = not self._get_val(args[0])
            elif op == "jmp":
                self.ip = self.labels[result]; continue
            elif op == "jz":
                cond = self._get_val(args[0])
                if not cond:
                    self.ip = self.labels[result]; continue
            elif op == "jnz":
                if self._get_val(args[0]):
                    self.ip = self.labels[result]; continue
            elif op == "print_":
                val = self._get_val(args[0])
                self.output.append(str(val))
            elif op == "alloc":
                self.memory[result] = self._default_val(args[1])
            elif op == "alloc_array":
                sz = int(args[2]) if len(args) > 2 else 0
                self.arrays[result] = [self._default_val(args[1]) for _ in range(sz)]
                self.memory[result] = 0
            elif op == "load":
                idx = int(self._get_val(args[1]))
                self.memory[result] = self.arrays.get(args[0], [])[idx] if args[0] in self.arrays else 0
            elif op == "store":
                idx = int(self._get_val(args[1]))
                if args[0] in self.arrays:
                    self.arrays[args[0]][idx] = self._get_val(args[2])
            elif op == "param":
                self.param_stack.append(self._get_val(args[0]))
            elif op == "call":
                func_name = args[0]
                n_params = int(args[1]) if len(args) > 1 else 0
                # 从param_stack中取出参数
                params = []
                for _ in range(n_params):
                    if self.param_stack:
                        params.append(self.param_stack.pop())
                params.reverse()

                if func_name == "print":
                    for p in params:
                        self.output.append(str(p))
                    if result:
                        self.memory[result] = None
                elif func_name in self.labels:
                    # 保存返回地址
                    self.ret_stack.append(self.ip)
                    target_ip = self.labels[func_name]
                    param_names = self._get_func_params_at(target_ip)
                    # ★ 修复: 保存整个内存快照，而非仅参数变量
                    self.saved_mem.append(dict(self.memory))
                    # 设置被调用函数的参数
                    for pname in param_names:
                        if params:
                            self.memory[pname] = params.pop(0)
                    # 跳转到函数体
                    self.ip = self._find_func_start(target_ip)
                    continue  # 跳过 self.ip += 1
                else:
                    if result:
                        self.memory[result] = 0
            elif op == "ret":
                ret_val = self._get_val(args[0])
                # ★ 修复: 用完整内存快照替换当前内存
                if self.saved_mem:
                    self.memory = self.saved_mem.pop()
                # 返回到调用者，将返回值存入调用指令的result
                if self.ret_stack:
                    caller_ip = self.ret_stack.pop()
                    caller_inst = self.instructions[caller_ip]
                    caller_result = caller_inst.get("result", "")
                    if caller_result:
                        self.memory[caller_result] = ret_val
                    self.ip = caller_ip
            elif op == "retv":
                # ★ 修复: 用完整内存快照替换当前内存
                if self.saved_mem:
                    self.memory = self.saved_mem.pop()
                if self.ret_stack:
                    self.ip = self.ret_stack.pop()
            elif op == "toFloat":
                self.memory[result] = float(self._get_val(args[0]))
            elif op == "toInt":
                self.memory[result] = int(self._get_val(args[0]))
            else:
                pass

            self.ip += 1
        return self.output

    def _get_func_params_at(self, target_ip):
        """获取函数入口处的参数名列表（alloc指令的result字段）"""
        params = []
        j = target_ip + 1  # 跳过label
        while j < len(self.instructions):
            inst = self.instructions[j]
            op = inst.get("op", "")
            if op == "enter_func":
                j += 1
                continue
            elif op == "alloc" or op == "alloc_array":
                params.append(inst.get("result", ""))
                j += 1
            else:
                break
        return params

    def _find_func_start(self, target_ip):
        """找到函数体的第一条实际指令（跳过label, enter_func, alloc序言）"""
        j = target_ip + 1
        while j < len(self.instructions):
            inst = self.instructions[j]
            op = inst.get("op", "")
            if op in ("enter_func", "alloc", "alloc_array"):
                j += 1
            elif op == "label":
                j += 1
            else:
                break
        return j

    def _get_val(self, arg):
        """获取操作数的值 — 先查内存，再解析字面量，否则返回0"""
        if arg in self.memory:
            return self.memory[arg]
        # 尝试解析为字面量（数字或布尔值）
        try:
            return self._parse_val(arg)
        except (ValueError, TypeError):
            pass
        # 变量尚未初始化，返回默认值0
        return 0

    def _parse_val(self, s):
        if s == "true": return True
        if s == "false": return False
        try:
            if "." in str(s): return float(s)
            return int(s)
        except (ValueError, TypeError):
            return str(s).strip('"')

    def _default_val(self, t):
        if t in ("int", "auto"): return 0
        if t == "float": return 0.0
        if t == "string": return ""
        if t == "bool": return False
        return 0

    def _arith(self, op, args):
        a = self._get_val(args[0])
        b = self._get_val(args[1]) if len(args) > 1 else 0
        if op == "add": return a + b
        if op == "sub": return a - b
        if op == "mul": return a * b
        if op == "div":
            if isinstance(a, int) and isinstance(b, int): return a // b
            return a / b
        if op == "mod": return a % b
        return 0

    def _cmp(self, op, args):
        a = self._get_val(args[0])
        b = self._get_val(args[1])
        if op == "lt": return a < b
        if op == "le": return a <= b
        if op == "gt": return a > b
        if op == "ge": return a >= b
        if op == "eq": return a == b
        if op == "ne": return a != b
        return False

    def _logic(self, op, args):
        a = bool(self._get_val(args[0]))
        b = bool(self._get_val(args[1]))
        if op == "and_": return a and b
        if op == "or_": return a or b
        return False


# ============================================================
# 便捷接口
# ============================================================

def generate_code(ast):
    """便捷入口：从AST生成TAC指令列表"""
    gen = TACGen()
    return gen.generate(ast)


def optimize_code(instructions):
    """便捷入口：优化TAC指令列表"""
    opt = TACOptimizer(instructions)
    return opt.optimize()


def run_code(instructions):
    """便捷入口：执行TAC指令列表"""
    interp = TACInterpreter(instructions)
    return interp.run()
