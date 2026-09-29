import sys
import json
import re
import os

TOKEN_SPECS = [
    ('MULTI_COMMENT', r'/\*[\s\S]*?\*/'),#先匹配正常的多行注释，再匹配未闭合的多行注释，否则会把整个剩余文本都当成一个未闭合注释
    ('UNCLOSED_COMMENT', r'/\*[\s\S]*'),#匹配未闭合的多行注释
    ('COMMENT', r'//[^\n]*'),#单行注释
    ('STRING', r'"(?:\\.|[^"\n\\])*"'),#先匹配正常的字符串，再匹配未闭合的字符串，否则会把整个剩余文本都当成一个未闭合字符串
    ('UNCLOSED_STRING', r'"(?:\\.|[^"\n\\])*(?:\n|$)'),#匹配未闭合的字符串
    ('INVALID_NUMBER', r'\b\d+\.[0-9.]+\.[0-9a-zA-Z_.]*|\b\d+[a-zA-Z_][a-zA0-9_]*\b|\b0[0-9]+\b'),#先匹配无效的浮点数（包含多个小数点），再匹配以数字开头但包含字母或下划线的无效标识符，最后匹配以0开头的无效整数（八进制）
    ('NUM', r'\b\d+\.\d+\b|\b\d+\b'),#先匹配合法的浮点数，再匹配合法的整数
    ('KEYWORD', r'\b(fn|void|int|float|string|bool|return|break|continue|if|else|while|true|false)\b'),#关键词
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),#标识符
    ('OP', r'->|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!]'),#操作符，先匹配多字符操作符，再匹配单字符操作符
    ('DELIM', r'[@:(),\[\].]'),#分隔符
    ('WHITESPACE', r'[ \t\r]+'),#空白字符（不包括换行）
    ('NEWLINE_TOKEN', r'\n'),#换行符，单独作为一个token类型，虽然不要求输出，但在计算行号时需要识别
    ('ILLEGAL_CHAR', r'.')#匹配任何其他未定义的单个字符，放在最后以确保其他规则优先匹配
]

tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECS)
get_token = re.compile(tok_regex).finditer
def tokenize(source_code):
    tokens = []
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
        elif kind == 'NEWLINE_TOKEN':
            continue
        if kind == 'UNCLOSED_COMMENT':
            errors.append({"type": "UNCLOSED_COMMENT", "value": value, "line": start_line, "col": start_col})
        elif kind == 'UNCLOSED_STRING':
            errors.append({"type": "UNCLOSED_STRING", "value": value, "line": start_line, "col": start_col})
        elif kind == 'INVALID_NUMBER':
            errors.append({"type": "INVALID_NUMBER", "value": value, "line": start_line, "col": start_col})
        elif kind == 'ILLEGAL_CHAR':
            errors.append({"type": "ILLEGAL_CHAR", "value": value, "line": start_line, "col": start_col})
        else:
            tokens.append({"type": kind, "value": value, "line": start_line, "col": start_col})
            
    tokens.append({"type": "EOF", "value": "", "line": current_line, "col": current_col})
    
    return {"tokens": tokens, "errors": errors}

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py tokenize <input.src>")
        print("       python compiler.py visualize-dfa")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "visualize-dfa":
        import visualizer
        visualizer.visualize()
        return

    if command != 'tokenize' or len(sys.argv) < 3:
        print("Usage: python compiler.py tokenize <input.src>")
        sys.exit(1)
        
    input_file = sys.argv[2]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)
        
    with open(input_file, 'r', encoding='utf-8') as f:
        source_code = f.read()
        
    result = tokenize(source_code)
    # print(json.dumps(result, ensure_ascii=False, indent=2))

    def format_items(items):
        """将 Token/Error 列表格式化为紧凑 JSON 字符串行，每行一个对象"""
        lines = []
        for i, item in enumerate(items):
            compact = json.dumps(item, ensure_ascii=False)
            comma = "," if i < len(items) - 1 else ""
            lines.append(f"    {compact}{comma}")
        return "\n".join(lines)

    if result["tokens"]:
        tokens_json = format_items(result["tokens"])
        tokens_part = f'"tokens": [\n{tokens_json}\n  ]'
    else:
        tokens_part = '"tokens": []'

    if result["errors"]:
        errors_json = format_items(result["errors"])
        errors_part = f'"errors": [\n{errors_json}\n  ]'
    else:
        errors_part = '"errors": []'

    output = (
        "{\n"
        f'  {tokens_part},\n'
        f'  {errors_part}\n'
        "}"
    )
    print(output)

if __name__ == "__main__":
    main()
