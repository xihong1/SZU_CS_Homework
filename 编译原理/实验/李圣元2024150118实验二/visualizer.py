class State:
    _id_cnt = 0
    def __init__(self):
        self.id = State._id_cnt
        State._id_cnt += 1
        self.transitions = {} 
        self.epsilon_transitions = set()

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def insert_concat(r):
    res = ""
    for i in range(len(r)):
        res += r[i]
        if i + 1 < len(r):
            c1 = r[i]
            c2 = r[i+1]
            if c1 not in '(|' and c2 not in ')|*':
                res += '.'
    return res

def to_postfix(exp):
    prec = {'*': 3, '.': 2, '|': 1, '(': 0}
    output = []
    stack = []
    for c in exp:
        if c.isalpha() or c.isdigit():
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and prec.get(stack[-1], 0) >= prec.get(c, 0):
                output.append(stack.pop())
            stack.append(c)
    while stack:
        output.append(stack.pop())
    return "".join(output)

def build_nfa(postfix):
    stack = []
    State._id_cnt = 0
    for c in postfix:
        if c == '.':
            n2 = stack.pop()
            n1 = stack.pop()
            n1.end.epsilon_transitions.add(n2.start)
            stack.append(NFA(n1.start, n2.end))
        elif c == '|':
            n2 = stack.pop()
            n1 = stack.pop()
            s = State()
            e = State()
            s.epsilon_transitions.update([n1.start, n2.start])
            n1.end.epsilon_transitions.add(e)
            n2.end.epsilon_transitions.add(e)
            stack.append(NFA(s, e))
        elif c == '*':
            n = stack.pop()
            s = State()
            e = State()
            s.epsilon_transitions.update([n.start, e])
            n.end.epsilon_transitions.update([n.start, e])
            stack.append(NFA(s, e))
        else:
            s = State()
            e = State()
            s.transitions.setdefault(c, set()).add(e)
            stack.append(NFA(s, e))
    return stack[0]

def e_closure(states):
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for e_state in state.epsilon_transitions:
            if e_state not in closure:
                closure.add(e_state)
                stack.append(e_state)
    return frozenset(closure)

def move(states, char):
    next_states = set()
    for state in states:
        if char in state.transitions:
            next_states.update(state.transitions[char])
    return next_states

def nfa_to_dfa(nfa, alphabet):
    start_closure = e_closure({nfa.start})
    dfa_states = [start_closure]
    dfa_transitions = {}
    unmarked = [start_closure]
    
    while unmarked:
        T = unmarked.pop(0)
        dfa_transitions[T] = {}
        for a in alphabet:
            U = e_closure(move(T, a))
            if not U: continue
            if U not in dfa_states:
                dfa_states.append(U)
                unmarked.append(U)
            dfa_transitions[T][a] = U
    return dfa_states, dfa_transitions

def visualize():
    # 以 ID (包含字母L和数字D) 与 数字(仅数字D) 的组合正则表达式作为词法规则示例
    # 模拟标识符与常数类型的识别: L(L|D)* | DD*
    regex = "(L(L|D)*)|(DD*)"
    alphabet = ['L', 'D']
    
    print(f"正在将词法规则转换: {regex}")
    print("字母表定义: L (Letter, 代表[a-zA-Z_]), D (Digit, 代表[0-9])\n")
    
    concat_r = insert_concat(regex)
    postfix = to_postfix(concat_r)
    nfa = build_nfa(postfix)
    dfa_states, transitions = nfa_to_dfa(nfa, alphabet)
    
    state_idx = {s: f"q{i}" for i, s in enumerate(dfa_states)}
    
    print("[1] === DFA 状态转换表 ===")
    header = "状态(State)\t" + "\t".join(f"字符 '{a}'" for a in alphabet) + "\t是否接受(Accept)"
    print("-" * 65)
    print(header)
    print("-" * 65)
    
    for state in dfa_states:
        is_accept = nfa.end in state
        row = [state_idx[state]]
        for a in alphabet:
            target = transitions[state].get(a)
            if target:
                row.append(state_idx[target])
            else:
                row.append("-")
        row.append("是" if is_accept else "否")
        print("\t\t".join(row))
        
    print("-" * 65)
    
    print("\n[2] === Markdown Mermaid 图示代码 ===")
    print("请将以下代码块直接复制到你的 Markdown 实验报告中，即可获得可视化的自动机图示：\n")
    print("```mermaid")
    print("stateDiagram-v2")
    print("    direction LR")
    print("    classDef accept fill:#e2f0e2,stroke:#333,stroke-width:2px;")
    
    # 标记接受状态
    for state in dfa_states:
        s_name = state_idx[state]
        if nfa.end in state:
            print(f"    {s_name}:::accept")
            
    # 连接起始状态
    print(f"    [*] --> {state_idx[dfa_states[0]]}")
    
    # 画边
    for state in dfa_states:
        s_name = state_idx[state]
        for a in alphabet:
            target = transitions[state].get(a)
            if target:
                t_name = state_idx[target]
                print(f"    {s_name} --> {t_name} : {a}")
    print("```")
