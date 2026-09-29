"""
NovaLang 编译器 - 实验四：语义分析与类型系统
支持命令：
  python compiler.py tokenize <input.src>   - 词法分析
  python compiler.py parse <input.src>      - 语法分析
  python compiler.py check <input.src>      - 语义分析
"""

import sys
import json
import re
import os

# ---- 词法分析器 ----

TOKEN_SPECS = [
    ('MULTI_COMMENT', r'/\*[\s\S]*?\*/'),
    ('UNCLOSED_COMMENT', r'/\*[\s\S]*'),
    ('COMMENT', r'//[^\n]*'),
    ('STRING', r'"(?:\\.|[^"\n\\])*"'),
    ('UNCLOSED_STRING', r'"(?:\\.|[^"\n\\])*(?:\n|$)'),
    ('INVALID_NUMBER', r'\b\d+\.[0-9.]+\.[0-9a-zA-Z_.]*|\b\d+[a-zA-Z_][a-zA0-9_]*\b|\b0[0-9]+\b'),
    ('NUM', r'\b\d+\.\d+\b|\b\d+\b'),
    ('KEYWORD', r'\b(fn|void|int|float|string|bool|auto|return|break|continue|if|else|while|true|false)\b'),
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OP', r'->|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!]'),
    ('DELIM', r'[@:(),\[\].]'),
    ('WHITESPACE', r'[ \t\r]+'),
    ('NEWLINE_TOKEN', r'\n'),
    ('ILLEGAL_CHAR', r'.')
]

tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECS)
get_token = re.compile(tok_regex).finditer


def tokenize_raw(source_code):
    raw_tokens = []
    errors = []
    current_line = 1
    current_col = 1
    for m in get_token(source_code):
        kind = m.lastgroup
        value = m.group()
        start_line = current_line
        start_col = current_col
        lines = value.split('\n')
        if len(lines) > 1:
            current_line += len(lines) - 1
            current_col = len(lines[-1]) + 1
        else:
            current_col += len(value)
        if kind == 'WHITESPACE':
            continue
        elif kind == 'COMMENT' or kind == 'MULTI_COMMENT':
            continue
        if kind == 'UNCLOSED_COMMENT':
            errors.append({"type": "UNCLOSED_COMMENT", "value": value, "line": start_line, "col": start_col})
            continue
        elif kind == 'UNCLOSED_STRING':
            errors.append({"type": "UNCLOSED_STRING", "value": value, "line": start_line, "col": start_col})
            continue
        elif kind == 'INVALID_NUMBER':
            errors.append({"type": "INVALID_NUMBER", "value": value, "line": start_line, "col": start_col})
            continue
        elif kind == 'ILLEGAL_CHAR':
            errors.append({"type": "ILLEGAL_CHAR", "value": value, "line": start_line, "col": start_col})
            continue
        elif kind == 'NEWLINE_TOKEN':
            raw_tokens.append({"type": "NEWLINE", "value": "\n", "line": start_line, "col": start_col})
            continue
        else:
            raw_tokens.append({"type": kind, "value": value, "line": start_line, "col": start_col})
    return raw_tokens, errors


def add_indent_tokens(raw_tokens):
    result = []
    indent_stack = [0]
    after_newline = True

    def compute_indent(tok):
        return tok["col"] - 1

    i = 0
    while i < len(raw_tokens):
        tok = raw_tokens[i]
        if tok["type"] == "NEWLINE":
            result.append(tok)
            after_newline = True
            i += 1
            continue
        if after_newline:
            after_newline = False
            indent = compute_indent(tok)
            current_indent = indent_stack[-1]
            if indent > current_indent:
                indent_stack.append(indent)
                result.append({"type": "INDENT", "value": "", "line": tok["line"], "col": 1})
            elif indent < current_indent:
                while indent_stack[-1] > indent:
                    indent_stack.pop()
                    result.append({"type": "DEDENT", "value": "", "line": tok["line"], "col": 1})
        result.append(tok)
        i += 1

    while len(indent_stack) > 1:
        indent_stack.pop()
        last_line = raw_tokens[-1]["line"] + 1 if raw_tokens else 1
        result.append({"type": "DEDENT", "value": "", "line": last_line, "col": 1})

    last_line = raw_tokens[-1]["line"] + 1 if raw_tokens else 1
    result.append({"type": "EOF", "value": "", "line": last_line, "col": 1})
    return result


def tokenize(source_code, with_indents=True):
    if with_indents:
        raw_tokens, errors = tokenize_raw(source_code)
        tokens = add_indent_tokens(raw_tokens)
    else:
        tokens, errors = tokenize_raw(source_code)
        tokens.append({"type": "EOF", "value": "", "line": 1, "col": 1})
    return {"tokens": tokens, "errors": errors}


# ---- 语法分析器 ----

class ParseError(Exception):
    def __init__(self, expected, found, line, col, message=""):
        self.expected = expected
        self.found = found
        self.line = line
        self.col = col
        self.message = message


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return {"type": "EOF", "value": "", "line": 0, "col": 0}

    def advance(self):
        tok = self.peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def expect(self, type_, value=None):
        tok = self.peek()
        if tok["type"] != type_ or (value is not None and tok["value"] != value):
            raise ParseError(
                value if value else type_,
                f'{tok["type"]}:{tok["value"]}',
                tok["line"],
                tok["col"],
            )
        return self.advance()

    def match(self, type_, value=None):
        tok = self.peek()
        if tok["type"] == type_ and (value is None or tok["value"] == value):
            return self.advance()
        return None

    def error(self, expected, found_tok):
        self.errors.append({
            "type": "SYNTAX_ERROR",
            "expected": expected,
            "found": found_tok["value"] or found_tok["type"],
            "line": found_tok["line"],
            "col": found_tok["col"],
            "message": f"expected '{expected}' before '{found_tok['value'] or found_tok['type']}'",
        })

    def recover_to_sync(self):
        while self.peek()["type"] not in ("NEWLINE", "EOF", "DEDENT"):
            self.advance()

    def skip_newlines(self):
        while self.peek()["type"] == "NEWLINE":
            self.advance()

    def is_stmt_start(self):
        tok = self.peek()
        if tok["type"] == "KEYWORD" and tok["value"] in (
            "if", "while", "return", "break", "continue", "fn",
            "int", "float", "string", "bool", "auto",
        ):
            return True
        return tok["type"] == "ID"

    def parse_program(self):
        funcs = []
        self.skip_newlines()
        while self.peek()["type"] != "EOF":
            if self.peek()["type"] == "DEDENT":
                self.advance()
                continue
            if self.peek()["type"] == "KEYWORD" and self.peek()["value"] == "fn":
                try:
                    funcs.append(self.parse_function_def())
                except ParseError as e:
                    self.error(e.expected, self.peek())
                    self.recover_to_sync()
                    self.skip_newlines()
            else:
                self.error("fn", self.peek())
                self.recover_to_sync()
                self.skip_newlines()
        return {
            "type": "Program",
            "funcs": funcs,
            "line": funcs[0]["line"] if funcs else 0,
            "col": funcs[0]["col"] if funcs else 0,
        }

    def parse_block_body(self):
        self.expect("NEWLINE")
        self.expect("INDENT")
        stmts = self.parse_statement_list()
        self.skip_newlines()
        if self.peek()["type"] != "DEDENT":
            while self.peek()["type"] not in ("DEDENT", "EOF"):
                self.advance()
        self.skip_newlines()
        if self.peek()["type"] == "DEDENT":
            self.advance()
        return stmts

    def parse_function_def(self):
        fn_tok = self.expect("KEYWORD", "fn")
        self.expect("DELIM", "(")
        ret_tok = self.peek()
        if ret_tok["type"] == "KEYWORD" and ret_tok["value"] in ("int", "float", "string", "bool", "void"):
            ret_type = self.advance()["value"]
        else:
            raise ParseError("type or void", f'{ret_tok["type"]}:{ret_tok["value"]}', ret_tok["line"], ret_tok["col"])
        self.expect("DELIM", ")")
        name_tok = self.expect("ID")
        self.expect("OP", "->")
        params = self.parse_param_list_opt()
        self.expect("DELIM", ":")
        body = self.parse_block_body()
        return {
            "type": "FuncDecl",
            "name": name_tok["value"],
            "return_type": ret_type,
            "params": params,
            "body": body,
            "line": fn_tok["line"],
            "col": fn_tok["col"],
        }

    def parse_param_list_opt(self):
        params = []
        if self.peek()["type"] == "ID":
            params.append(self.parse_param_decl())
            while self.match("DELIM", ","):
                params.append(self.parse_param_decl())
        return params

    def parse_param_decl(self):
        name_tok = self.expect("ID")
        self.expect("DELIM", "@")
        ptype = self.parse_type()
        array_size = None
        if self.match("DELIM", "["):
            size_tok = self.expect("NUM")
            self.expect("DELIM", "]")
            array_size = size_tok["value"]
        result = {
            "type": "ParamDecl",
            "name": name_tok["value"],
            "param_type": ptype,
            "line": name_tok["line"],
            "col": name_tok["col"],
        }
        if array_size is not None:
            result["array_size"] = array_size
        return result

    def parse_type(self):
        tok = self.peek()
        if tok["type"] == "KEYWORD" and tok["value"] in ("int", "float", "string", "bool"):
            self.advance()
            return tok["value"]
        raise ParseError("type", f'{tok["type"]}:{tok["value"]}', tok["line"], tok["col"])

    def parse_statement_list(self):
        stmts = []
        while True:
            if self.peek()["type"] in ("DEDENT", "EOF"):
                break
            if self.peek()["type"] == "NEWLINE":
                self.advance()
                continue
            if not self.is_stmt_start():
                break
            try:
                stmts.append(self.parse_statement())
            except ParseError as e:
                self.error(e.expected, self.peek())
                self.recover_to_sync()
                self.skip_newlines()
        return stmts

    def parse_statement(self):
        tok = self.peek()
        if tok["type"] == "KEYWORD" and tok["value"] == "if":
            return self.parse_if_stmt()
        elif tok["type"] == "KEYWORD" and tok["value"] == "while":
            return self.parse_while_stmt()
        elif tok["type"] == "KEYWORD" and tok["value"] == "return":
            return self.parse_return_stmt()
        elif tok["type"] == "KEYWORD" and tok["value"] == "break":
            self.advance()
            return {"type": "BreakStmt", "line": tok["line"], "col": tok["col"]}
        elif tok["type"] == "KEYWORD" and tok["value"] == "continue":
            self.advance()
            return {"type": "ContinueStmt", "line": tok["line"], "col": tok["col"]}
        elif tok["type"] == "KEYWORD" and tok["value"] in ("int", "float", "string", "bool"):
            return self.parse_var_decl()
        elif tok["type"] == "KEYWORD" and tok["value"] == "auto":
            return self.parse_auto_decl()
        elif tok["type"] == "ID":
            return self.parse_id_statement()
        return self.parse_expr_stmt()

    def parse_var_decl(self):
        type_tok = self.advance()
        name_tok = self.expect("ID")
        if self.match("DELIM", "["):
            size_tok = self.expect("NUM")
            self.expect("DELIM", "]")
            return {
                "type": "VarDecl", "var_type": type_tok["value"],
                "name": name_tok["value"], "size": size_tok["value"],
                "line": type_tok["line"], "col": type_tok["col"],
            }
        if self.match("OP", "="):
            init = self.parse_expr()
            return {
                "type": "VarDecl", "var_type": type_tok["value"],
                "name": name_tok["value"], "init": init,
                "line": type_tok["line"], "col": type_tok["col"],
            }
        return {
            "type": "VarDecl", "var_type": type_tok["value"],
            "name": name_tok["value"],
            "line": type_tok["line"], "col": type_tok["col"],
        }

    def parse_auto_decl(self):
        """解析 auto 类型推导声明: auto name = expr"""
        auto_tok = self.advance()  # 消费 'auto'
        name_tok = self.expect("ID")
        self.expect("OP", "=")
        init = self.parse_expr()
        return {
            "type": "AutoVarDecl",
            "name": name_tok["value"],
            "init": init,
            "line": auto_tok["line"],
            "col": auto_tok["col"],
        }

    def parse_id_statement(self):
        expr = self.parse_expr()
        if isinstance(expr, dict) and expr.get("type") in ("TypedVarRef", "TypedArrayElemRef") and self.match("OP", "="):
            value = self.parse_expr()
            return {
                "type": "AssignStmt", "target": expr, "value": value,
                "line": expr["line"], "col": expr["col"],
            }
        return {"type": "ExprStmt", "expr": expr, "line": expr["line"], "col": expr["col"]}

    def parse_if_stmt(self):
        if_tok = self.expect("KEYWORD", "if")
        cond = self.parse_expr()
        self.expect("DELIM", ":")
        then_body = self.parse_block_body()
        else_body = None
        if self.peek()["type"] == "NEWLINE":
            self.advance()
        if self.peek()["type"] == "KEYWORD" and self.peek()["value"] == "else":
            self.advance()
            self.expect("DELIM", ":")
            else_body = self.parse_block_body()
        return {
            "type": "IfStmt", "cond": cond, "then": then_body, "else": else_body,
            "line": if_tok["line"], "col": if_tok["col"],
        }

    def parse_while_stmt(self):
        while_tok = self.expect("KEYWORD", "while")
        cond = self.parse_expr()
        self.expect("DELIM", ":")
        body = self.parse_block_body()
        return {
            "type": "WhileStmt", "cond": cond, "body": body,
            "line": while_tok["line"], "col": while_tok["col"],
        }

    def parse_return_stmt(self):
        ret_tok = self.expect("KEYWORD", "return")
        expr = None
        if self.peek()["type"] not in ("NEWLINE", "EOF", "DEDENT"):
            expr = self.parse_expr()
        return {
            "type": "ReturnStmt", "expr": expr,
            "line": ret_tok["line"], "col": ret_tok["col"],
        }

    def parse_expr_stmt(self):
        expr = self.parse_expr()
        return {"type": "ExprStmt", "expr": expr, "line": expr["line"], "col": expr["col"]}

    def parse_expr(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.peek()["type"] == "OP" and self.peek()["value"] == "||":
            self.advance()
            right = self.parse_logical_and()
            left = {"type": "BinaryExpr", "op": "||", "left": left, "right": right,
                    "line": left["line"], "col": left["col"]}
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.peek()["type"] == "OP" and self.peek()["value"] == "&&":
            self.advance()
            right = self.parse_equality()
            left = {"type": "BinaryExpr", "op": "&&", "left": left, "right": right,
                    "line": left["line"], "col": left["col"]}
        return left

    def parse_equality(self):
        left = self.parse_relation()
        while self.peek()["type"] == "OP" and self.peek()["value"] in ("==", "!="):
            op = self.advance()
            right = self.parse_relation()
            left = {"type": "BinaryExpr", "op": op["value"], "left": left, "right": right,
                    "line": left["line"], "col": left["col"]}
        return left

    def parse_relation(self):
        left = self.parse_additive()
        while self.peek()["type"] == "OP" and self.peek()["value"] in ("<", "<=", ">", ">="):
            op = self.advance()
            right = self.parse_additive()
            left = {"type": "BinaryExpr", "op": op["value"], "left": left, "right": right,
                    "line": left["line"], "col": left["col"]}
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.peek()["type"] == "OP" and self.peek()["value"] in ("+", "-"):
            op = self.advance()
            right = self.parse_multiplicative()
            left = {"type": "BinaryExpr", "op": op["value"], "left": left, "right": right,
                    "line": left["line"], "col": left["col"]}
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.peek()["type"] == "OP" and self.peek()["value"] in ("*", "/", "%"):
            op = self.advance()
            right = self.parse_unary()
            left = {"type": "BinaryExpr", "op": op["value"], "left": left, "right": right,
                    "line": left["line"], "col": left["col"]}
        return left

    def parse_unary(self):
        tok = self.peek()
        if tok["type"] == "OP" and tok["value"] in ("!", "-"):
            op = self.advance()
            operand = self.parse_unary()
            return {"type": "UnaryExpr", "op": op["value"], "operand": operand,
                    "line": op["line"], "col": op["col"]}
        return self.parse_postfix()

    def parse_postfix(self):
        expr = self.parse_primary()
        while True:
            if self.peek()["type"] == "DELIM" and self.peek()["value"] == ".":
                self.advance()
                name_tok = self.expect("ID")
                if self.match("DELIM", "("):
                    args = self.parse_arg_list_opt()
                    self.expect("DELIM", ")")
                    expr = {"type": "MethodCall", "object": expr, "method": name_tok["value"],
                            "args": args, "line": expr["line"], "col": expr["col"]}
                else:
                    expr = {"type": "MemberAccess", "object": expr, "member": name_tok["value"],
                            "line": expr["line"], "col": expr["col"]}
            elif self.peek()["type"] == "OP" and self.peek()["value"] == "->":
                self.advance()
                self.expect("DELIM", "(")
                args = self.parse_arg_list_opt()
                self.expect("DELIM", ")")
                expr = {"type": "CallExpr", "callee": expr, "args": args,
                        "line": expr["line"], "col": expr["col"]}
            else:
                break
        return expr

    def parse_primary(self):
        tok = self.peek()
        if tok["type"] == "NUM":
            self.advance()
            if "." in tok["value"]:
                return {"type": "FloatLiteral", "value": tok["value"], "line": tok["line"], "col": tok["col"]}
            return {"type": "IntLiteral", "value": tok["value"], "line": tok["line"], "col": tok["col"]}
        elif tok["type"] == "STRING":
            self.advance()
            return {"type": "StringLiteral", "value": tok["value"], "line": tok["line"], "col": tok["col"]}
        elif tok["type"] == "KEYWORD" and tok["value"] in ("true", "false"):
            self.advance()
            return {"type": "BoolLiteral", "value": tok["value"], "line": tok["line"], "col": tok["col"]}
        elif tok["type"] == "DELIM" and tok["value"] == "(":
            self.advance()
            expr = self.parse_expr()
            self.expect("DELIM", ")")
            return expr
        elif tok["type"] == "ID":
            return self.parse_typed_ref_or_call()
        raise ParseError("expression", f'{tok["type"]}:{tok["value"]}', tok["line"], tok["col"])

    def parse_typed_ref_or_call(self):
        name_tok = self.expect("ID")
        if self.peek()["type"] == "DELIM" and self.peek()["value"] == "[":
            self.advance()
            idx = self.parse_expr()
            self.expect("DELIM", "]")
            self.expect("DELIM", "@")
            ref_type = self.parse_type()
            return {"type": "TypedArrayElemRef", "name": name_tok["value"], "index": idx,
                    "ref_type": ref_type, "line": name_tok["line"], "col": name_tok["col"]}
        if self.peek()["type"] == "DELIM" and self.peek()["value"] == "@":
            self.advance()
            ref_type = self.parse_type()
            if self.peek()["type"] == "DELIM" and self.peek()["value"] == "[":
                self.advance()
                size_tok = self.expect("NUM")
                self.expect("DELIM", "]")
                return {"type": "TypedArrayRef", "name": name_tok["value"], "ref_type": ref_type,
                        "size": size_tok["value"], "line": name_tok["line"], "col": name_tok["col"]}
            return {"type": "TypedVarRef", "name": name_tok["value"], "ref_type": ref_type,
                    "line": name_tok["line"], "col": name_tok["col"]}
        return {"type": "Identifier", "name": name_tok["value"],
                "line": name_tok["line"], "col": name_tok["col"]}

    def parse_arg_list_opt(self):
        if self.peek()["type"] == "DELIM" and self.peek()["value"] == ")":
            return []
        args = [self.parse_expr()]
        while self.match("DELIM", ","):
            args.append(self.parse_expr())
        return args

    def parse(self):
        ast = self.parse_program()
        return {"ast": ast, "errors": self.errors}


# ---- JSON 格式化输出 ----

def format_primitive(val):
    if isinstance(val, str):
        return json.dumps(val, ensure_ascii=False)
    elif isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, (int, float)):
        return str(val)
    elif val is None:
        return "null"
    return json.dumps(val, ensure_ascii=False)


def format_ast_compact(node, indent=0):
    pad = "  " * indent
    inner_pad = "  " * (indent + 1)
    if isinstance(node, dict):
        simple_fields = []
        complex_fields = []
        for k, v in node.items():
            if isinstance(v, (dict, list)):
                complex_fields.append((k, v))
            else:
                simple_fields.append((k, v))
        simple_parts = [f'"{k}": {format_primitive(v)}' for k, v in simple_fields]
        if not complex_fields:
            return "{ " + ", ".join(simple_parts) + " }"
        lines = ["{"]
        lines.append(inner_pad + ", ".join(simple_parts) + ",")
        for i, (k, v) in enumerate(complex_fields):
            comma = "," if i < len(complex_fields) - 1 else ""
            lines.append(f'{inner_pad}"{k}": {format_ast_compact(v, indent + 1)}{comma}')
        lines.append(pad + "}")
        return "\n".join(lines)
    elif isinstance(node, list):
        if not node:
            return "[]"
        lines = ["["]
        for i, item in enumerate(node):
            comma = "," if i < len(node) - 1 else ""
            lines.append(inner_pad + format_ast_compact(item, indent + 1) + comma)
        lines.append(pad + "]")
        return "\n".join(lines)
    else:
        return format_primitive(node)


def format_items(items):
    lines = []
    for i, item in enumerate(items):
        compact = format_ast_compact(item, indent=2)
        comma = "," if i < len(items) - 1 else ""
        lines.append(f"    {compact}{comma}")
    return "\n".join(lines)


def output_json(data):
    if "ast" in data and "errors" in data:
        if data["errors"]:
            ast_str = "null"
            errors_json = format_items(data["errors"])
            errors_part = f'"errors": [\n{errors_json}\n  ]'
        else:
            ast_str = format_ast_compact(data["ast"], indent=1)
            errors_part = '"errors": []'
        print("{\n" f'  "ast": {ast_str},\n' f'  {errors_part}\n' "}")
    elif "tokens" in data and "errors" in data:
        if data["tokens"]:
            tokens_json = format_items(data["tokens"])
            tokens_part = f'"tokens": [\n{tokens_json}\n  ]'
        else:
            tokens_part = '"tokens": []'
        if data["errors"]:
            errors_json = format_items(data["errors"])
            errors_part = f'"errors": [\n{errors_json}\n  ]'
        else:
            errors_part = '"errors": []'
        print("{\n" f'  {tokens_part},\n' f'  {errors_part}\n' "}")
    elif "symbols" in data and "errors" in data:
        # check 命令的输出
        errors = data.get("errors", [])
        symbols = data.get("symbols", [])
        if errors:
            errors_json = format_items(errors)
            errors_part = f'"errors": [\n{errors_json}\n  ]'
        else:
            errors_part = '"errors": []'
        if symbols:
            symbols_json = format_items(symbols)
            symbols_part = f'"symbols": [\n{symbols_json}\n  ]'
        else:
            symbols_part = '"symbols": []'
        print("{\n" f'  {errors_part},\n' f'  {symbols_part}\n' "}")


# ---- 主程序 ----

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py tokenize <input.src>")
        print("       python compiler.py parse <input.src>")
        print("       python compiler.py check <input.src>")
        sys.exit(1)

    command = sys.argv[1]

    if len(sys.argv) < 3:
        print(f"Usage: python compiler.py {command} <input.src>")
        sys.exit(1)

    input_file = sys.argv[2]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        source_code = f.read()

    if command == 'tokenize':
        result = tokenize(source_code, with_indents=False)
        output_json(result)

    elif command == 'parse':
        result = tokenize(source_code, with_indents=True)
        lex_errors = result["errors"]
        tokens = result["tokens"]
        parser = Parser(tokens)
        parse_result = parser.parse()
        all_errors = lex_errors + parse_result["errors"]
        ast = parse_result["ast"] if not all_errors else None
        output_json({"ast": ast, "errors": all_errors})

    elif command == 'check':
        # 词法分析
        result = tokenize(source_code, with_indents=True)
        lex_errors = result["errors"]
        tokens = result["tokens"]

        # 语法分析
        parser = Parser(tokens)
        parse_result = parser.parse()
        syntax_errors = parse_result["errors"]
        ast = parse_result["ast"]
        all_frontend_errors = lex_errors + syntax_errors

        if all_frontend_errors:
            # 词法/语法有错误时，无法进行语义分析
            output_json({
                "errors": all_frontend_errors,
                "symbols": [],
            })
        else:
            # 语义分析
            from semantic_module import semantic_check
            result = semantic_check(ast)
            output_json(result)

    else:
        print(f"Unknown command: {command}")
        print("Usage: python compiler.py tokenize <input.src>")
        print("       python compiler.py parse <input.src>")
        print("       python compiler.py check <input.src>")
        sys.exit(1)


if __name__ == "__main__":
    main()
