import sys
import json
import re
import os
from parser_module import Parser

TOKEN_SPECS = [
    ('MULTI_COMMENT', r'/\*[\s\S]*?\*/'),
    ('UNCLOSED_COMMENT', r'/\*[\s\S]*'),
    ('COMMENT', r'//[^\n]*'),
    ('STRING', r'"(?:\\.|[^"\n\\])*"'),
    ('UNCLOSED_STRING', r'"(?:\\.|[^"\n\\])*(?:\n|$)'),
    ('INVALID_NUMBER', r'\b\d+\.[0-9.]+\.[0-9a-zA-Z_.]*|\b\d+[a-zA-Z_][a-zA0-9_]*\b|\b0[0-9]+\b'),
    ('NUM', r'\b\d+\.\d+\b|\b\d+\b'),
    ('KEYWORD', r'\b(fn|void|int|float|string|bool|return|break|continue|if|else|while|true|false)\b'),
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
        result.append({"type": "DEDENT", "value": "", "line": raw_tokens[-1]["line"] + 1 if raw_tokens else 1, "col": 1})

    result.append({"type": "EOF", "value": "", "line": raw_tokens[-1]["line"] + 1 if raw_tokens else 1, "col": 1})
    return result


def tokenize(source_code, with_indents=True):
    if with_indents:
        raw_tokens, errors = tokenize_raw(source_code)
        tokens = add_indent_tokens(raw_tokens)
    else:
        tokens, errors = tokenize_raw(source_code)
        tokens.append({"type": "EOF", "value": "", "line": 1, "col": 1})
    return {"tokens": tokens, "errors": errors}


def format_primitive(val):
    """Format a primitive JSON value (string, number, bool, null)."""
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
    """Format an AST node in compact style.

    Simple fields (strings, numbers, bools, null) go on the first line.
    Complex fields (dicts, lists) each go on their own indented line.
    Nodes with no complex fields render entirely on one line.
    """
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
    """Format a list of items (tokens or errors) compactly (each on one line)."""
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py tokenize <input.src>")
        print("       python compiler.py parse <input.src>")
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
    else:
        print(f"Unknown command: {command}")
        print("Usage: python compiler.py tokenize <input.src>")
        print("       python compiler.py parse <input.src>")
        sys.exit(1)


if __name__ == "__main__":
    main()
