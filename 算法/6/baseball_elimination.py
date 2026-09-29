"""
棒球淘汰问题 - 基于最大流算法的求解
Baseball Elimination Problem using Maximum Flow

实验六：最大流应用问题
"""

from collections import defaultdict, deque
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class MaxFlowSolver:
    """
    最大流求解器 - 使用Dinic算法
    
    Dinic算法核心思想：
    1. 构建分层图(BFS)：找到从源点到汇点的所有最短路径
    2. 在分层图上进行DFS阻塞流：找到所有增广路径
    3. 重复直到无法找到增广路径
    
    时间复杂度：O(V²E)，比Edmonds-Karp的O(VE²)更优
    """
    
    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(dict)
        self.flow = defaultdict(dict)
    
    def add_edge(self, u, v, cap):
        """添加有向边"""
        self.graph[u][v] = cap
        self.graph[v][u] = 0
        self.flow[u][v] = 0
        self.flow[v][u] = 0
    
    def bfs(self, s, t, level):
        """BFS构建分层图"""
        for i in range(self.n):
            level[i] = -1
        level[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if level[v] == -1 and self.graph[u][v] - self.flow[u][v] > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[t] != -1
    
    def dfs(self, u, t, flow, level, start):
        """DFS寻找增广路径"""
        if u == t:
            return flow
        while start[u] < len(self.graph[u]):
            v = list(self.graph[u].keys())[start[u]]
            if level[v] == level[u] + 1 and self.graph[u][v] - self.flow[u][v] > 0:
                pushed = self.dfs(v, t, min(flow, self.graph[u][v] - self.flow[u][v]), level, start)
                if pushed > 0:
                    self.flow[u][v] += pushed
                    self.flow[v][u] -= pushed
                    return pushed
            start[u] += 1
        return 0
    
    def max_flow(self, s, t):
        """Dinic最大流算法主函数"""
        total_flow = 0
        level = [-1] * self.n
        while self.bfs(s, t, level):
            start = [0] * self.n
            while True:
                pushed = self.dfs(s, t, float('inf'), level, start)
                if pushed == 0:
                    break
                total_flow += pushed
        return total_flow


class BaseballElimination:
    """
    棒球淘汰问题求解器
    
    流网络构造原理：
    1. 源点s连接到每个"比赛节点"，容量为该场比赛的剩余场次数
    2. 每个"比赛节点"连接到参赛的两支球队，容量为无穷大
    3. 每支球队连接到汇点t，容量为该球队最多能赢的场数减去当前胜场数
    
    判定淘汰的原理：
    - 如果最大流等于所有剩余比赛场次之和，说明所有比赛都能安排
    - 如果最大流小于总剩余比赛场次，说明无法安排所有比赛，该球队被淘汰
    """
    
    def __init__(self):
        self.teams = []
        self.wins = {}
        self.losses = {}
        self.remaining = {}
        self.against = {}
    
    def add_team(self, name, wins, losses, remaining, against):
        """添加球队信息"""
        self.teams.append(name)
        self.wins[name] = wins
        self.losses[name] = losses
        self.remaining[name] = remaining
        self.against[name] = against
    
    def solve(self, team_name):
        """
        判断指定球队是否被淘汰
        
        构建流网络：
        - 节点分配：0=源点, 1~k=比赛节点, k+1~k+n=球队节点, k+n+1=汇点
        - 比赛节点数：C(n,2) = n*(n-1)/2
        """
        n = len(self.teams)
        if team_name not in self.teams:
            return False, 0, 0
        
        # 计算该球队最多能赢多少场
        max_wins = self.wins[team_name] + self.remaining[team_name]
        
        # 检查是否有球队当前胜场已经超过该球队最多能赢的场数
        for other in self.teams:
            if other != team_name and self.wins[other] > max_wins:
                return True, 0, 0
        
        # 节点编号
        # 0: 源点
        # 1 ~ num_games: 比赛节点
        # num_games+1 ~ num_games+n: 球队节点
        # num_games+n+1: 汇点
        num_games = 0
        game_pairs = []
        for i in range(n):
            for j in range(i+1, n):
                if self.teams[i] != team_name and self.teams[j] != team_name:
                    game_pairs.append((self.teams[i], self.teams[j]))
                    num_games += 1
        
        source = 0
        sink = num_games + n + 1
        total_nodes = sink + 1
        
        solver = MaxFlowSolver(total_nodes)
        
        # 添加源点到比赛节点的边
        total_remaining = 0
        for idx, (t1, t2) in enumerate(game_pairs):
            game_node = idx + 1
            # 获取比赛场次数，需要检查两个方向
            cap = self.against[t1].get(t2, 0) + self.against[t2].get(t1, 0)
            solver.add_edge(source, game_node, cap)
            total_remaining += cap
            
            # 比赛节点到两支球队的边
            t1_idx = num_games + self.teams.index(t1) + 1
            t2_idx = num_games + self.teams.index(t2) + 1
            solver.add_edge(game_node, t1_idx, float('inf'))
            solver.add_edge(game_node, t2_idx, float('inf'))
        
        # 添加球队节点到汇点的边
        for i, team in enumerate(self.teams):
            if team != team_name:
                team_node = num_games + i + 1
                cap = max_wins - self.wins[team]
                if cap < 0:
                    return True, 0, 0
                solver.add_edge(team_node, sink, cap)
        
        # 计算最大流
        flow = solver.max_flow(source, sink)
        
        eliminated = flow < total_remaining
        return eliminated, flow, total_remaining
    
    def solve_all(self):
        """求解所有球队的淘汰情况"""
        results = {}
        for team in self.teams:
            eliminated, flow, total = self.solve(team)
            results[team] = {
                'eliminated': eliminated,
                'flow': flow,
                'total_remaining': total,
                'max_wins': self.wins[team] + self.remaining[team]
            }
        return results


def create_example1():
    """
    创建实验内容中的第一个例子（NL West 1996年9月8日）
    四支球队的比赛情况
    """
    elim = BaseballElimination()
    
    # 球队名称，胜场，负场，剩余场次
    # against字典：{对手: 剩余对战场次}
    elim.add_team('Atlanta', 83, 71, 8, {'Philly': 1, 'NY': 6, 'Montreal': 1})
    elim.add_team('Philly', 80, 79, 3, {'Atlanta': 1, 'NY': 0, 'Montreal': 2})
    elim.add_team('NY', 78, 78, 6, {'Atlanta': 6, 'Philly': 0, 'Montreal': 0})
    elim.add_team('Montreal', 77, 82, 3, {'Atlanta': 1, 'Philly': 2, 'NY': 0})
    
    return elim


def create_example2():
    """
    创建普林斯顿大学测试数据格式的例子
    """
    elim = BaseballElimination()
    
    elim.add_team('Atlanta', 83, 71, 8, {'Philly': 1, 'NY': 6, 'Montreal': 1})
    elim.add_team('Philly', 80, 79, 3, {'Atlanta': 1, 'NY': 0, 'Montreal': 2})
    elim.add_team('NY', 78, 78, 6, {'Atlanta': 6, 'Philly': 0, 'Montreal': 0})
    elim.add_team('Montreal', 77, 82, 3, {'Atlanta': 1, 'Philly': 2, 'NY': 0})
    
    return elim


def visualize_results(results, title="棒球淘汰问题求解结果"):
    """可视化求解结果"""
    teams = list(results.keys())
    eliminated = [results[t]['eliminated'] for t in teams]
    max_wins = [results[t]['max_wins'] for t in teams]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 左图：淘汰状态
    colors = ['red' if e else 'green' for e in eliminated]
    bars = axes[0].bar(teams, [1]*len(teams), color=colors)
    axes[0].set_title('球队淘汰状态', fontsize=14)
    axes[0].set_ylabel('状态')
    axes[0].set_yticks([])
    
    # 添加标签
    for bar, team, elim in zip(bars, teams, eliminated):
        status = '已淘汰' if elim else '未淘汰'
        axes[0].text(bar.get_x() + bar.get_width()/2, 0.5, status,
                    ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 右图：最大可能胜场数
    colors2 = ['red' if results[t]['eliminated'] else 'blue' for t in teams]
    bars2 = axes[1].bar(teams, max_wins, color=colors2)
    axes[1].set_title('各队最大可能胜场数', fontsize=14)
    axes[1].set_ylabel('胜场数')
    
    # 添加数值标签
    for bar, val in zip(bars2, max_wins):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(val), ha='center', va='bottom', fontsize=10)
    
    plt.suptitle(title, fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('baseball_elimination_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("结果图已保存为 baseball_elimination_results.png")


def visualize_flow_network(team_name, elim):
    """可视化流网络结构 - 清晰的专业版"""
    import matplotlib.patches as mpatches
    import matplotlib.font_manager as fm

    n = len(elim.teams)
    max_wins = elim.wins[team_name] + elim.remaining[team_name]

    # ── Chinese font setup ──
    cn_font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
    fm.fontManager.addfont(cn_font_path)
    cn_font_name = fm.FontProperties(fname=cn_font_path).get_name()
    matplotlib.rcParams['font.family'] = cn_font_name
    cn_font = fm.FontProperties(fname=cn_font_path)

    # ── Build network data ──
    other_teams = [t for t in elim.teams if t != team_name]
    game_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if elim.teams[i] != team_name and elim.teams[j] != team_name:
                g = elim.against[elim.teams[i]].get(elim.teams[j], 0)
                if g > 0:
                    game_pairs.append((elim.teams[i], elim.teams[j], g))

    n_games = len(game_pairs)
    n_teams = len(other_teams)

    # ── Layout constants ──
    COL_SRC = 0
    COL_GAME = 3.5
    COL_TEAM = 7.5
    COL_SINK = 11

    total_rows = max(n_games, n_teams, 1)
    spacing = min(2.5, 7.0 / total_rows)

    def y_pos(idx, total):
        if total <= 1:
            return 0.5
        return (total - 1) * spacing / 2 - idx * spacing

    # ── Figure ──
    fig, ax = plt.subplots(figsize=(18, max(8, total_rows * 2.2 + 4)))

    # ── Layer backgrounds ──
    layers = [
        (-1.0, COL_SRC, '源点层\nSource', '#C8E6C9'),
        (COL_SRC + 1.5, COL_GAME, '比赛节点层\nGame Nodes', '#BBDEFB'),
        (COL_GAME + 1.5, COL_TEAM, '球队节点层\nTeam Nodes', '#FFE0B2'),
        (COL_TEAM + 1.5, COL_SINK, '汇点层\nSink', '#FFCDD2'),
    ]
    y_min_val = y_pos(total_rows - 1, total_rows) - 1.8
    y_max_val = y_pos(0, total_rows) + 1.8
    for x_left, x_right, label, color in layers:
        rect = plt.Rectangle((x_left, y_min_val), x_right - x_left,
                              y_max_val - y_min_val, facecolor=color,
                              edgecolor='#BDBDBD', linewidth=1.5,
                              linestyle='--', alpha=0.45, zorder=1)
        ax.add_patch(rect)
        ax.text((x_left + x_right) / 2, y_min_val - 0.35, label,
                fontsize=14, ha='center', va='top', fontweight='bold',
                color='#616161', fontproperties=cn_font)

    # ── Node positions ──
    pos = {}
    pos['s'] = (COL_SRC, y_pos(0, 2))

    for i, (t1, t2, g) in enumerate(game_pairs):
        pos[f'g_{t1}_{t2}'] = (COL_GAME, y_pos(i, n_games))

    for i, t in enumerate(other_teams):
        pos[f't_{t}'] = (COL_TEAM, y_pos(i, n_teams))

    pos['t'] = (COL_SINK, y_pos(0, 2))

    # ── Colors ──
    C_SRC = '#2E7D32'
    C_GAME = '#1565C0'
    C_TEAM = '#E65100'
    C_SINK = '#C62828'
    C_GRAY = '#757575'

    # ── Source → Game edges ──
    for t1, t2, g in game_pairs:
        u = f'g_{t1}_{t2}'
        ax.annotate('', xy=pos[u], xytext=pos['s'],
                    arrowprops=dict(arrowstyle='->', color=C_SRC, lw=3,
                                   connectionstyle='arc3,rad=0'))
        mx = (pos['s'][0] + pos[u][0]) / 2
        my = (pos['s'][1] + pos[u][1]) / 2
        ax.text(mx, my + 0.3, f'c={g}', fontsize=15, color='#1B5E20',
                ha='center', fontweight='bold')

    # ── Game → Team edges ──
    for t1, t2, g in game_pairs:
        u = f'g_{t1}_{t2}'
        for t in [t1, t2]:
            v = f't_{t}'
            if v not in pos:
                continue
            dy = pos[v][1] - pos[u][1]
            rad = -0.2 if dy > 0 else 0.2 if dy < 0 else 0
            ax.annotate('', xy=pos[v], xytext=pos[u],
                        arrowprops=dict(arrowstyle='->', color=C_GRAY, lw=2,
                                       connectionstyle=f'arc3,rad={rad}'))
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            offset = 0.4 if rad <= 0 else -0.4
            ax.text(mid_x, mid_y + offset, '∞', fontsize=16,
                    color='#616161', ha='center', fontweight='bold')

    # ── Team → Sink edges ──
    for i, t in enumerate(other_teams):
        u = f't_{t}'
        cap = max_wins - elim.wins[t]
        rad = 0.15 * (i - (n_teams - 1) / 2) / max(1, n_teams - 1)
        ax.annotate('', xy=pos['t'], xytext=pos[u],
                    arrowprops=dict(arrowstyle='->', color=C_SINK, lw=3,
                                   connectionstyle=f'arc3,rad={rad}'))
        mx = pos[u][0] * 0.5 + pos['t'][0] * 0.5
        my = pos[u][1] * 0.5 + pos['t'][1] * 0.5
        ax.text(mx, my + 0.35,
                f'c = {max_wins} − {elim.wins[t]} = {cap}',
                fontsize=14, color='#B71C1C', ha='center', fontweight='bold')

    # ── Draw nodes ──
    radius = 0.8

    # Source
    c = plt.Circle(pos['s'], radius, facecolor=C_SRC, edgecolor='white', linewidth=3, zorder=3)
    ax.add_patch(c)
    ax.text(pos['s'][0], pos['s'][1], '源点\ns', fontsize=16, ha='center',
            va='center', color='white', fontweight='bold', zorder=4, fontproperties=cn_font)

    # Game nodes
    for t1, t2, g in game_pairs:
        u = f'g_{t1}_{t2}'
        c = plt.Circle(pos[u], radius, facecolor=C_GAME, edgecolor='white', linewidth=3, zorder=3)
        ax.add_patch(c)
        label = f'{t1}\nvs\n{t2}\n(c={g})'
        ax.text(pos[u][0], pos[u][1], label, fontsize=11, ha='center',
                va='center', color='white', fontweight='bold', zorder=4)

    # Team nodes
    for t in other_teams:
        u = f't_{t}'
        cap = max_wins - elim.wins[t]
        c = plt.Circle(pos[u], radius, facecolor=C_TEAM, edgecolor='white', linewidth=3, zorder=3)
        ax.add_patch(c)
        label = f'{t}\n(w={elim.wins[t]})\ncap={cap}'
        ax.text(pos[u][0], pos[u][1], label, fontsize=11, ha='center',
                va='center', color='white', fontweight='bold', zorder=4)

    # Sink
    c = plt.Circle(pos['t'], radius, facecolor=C_SINK, edgecolor='white', linewidth=3, zorder=3)
    ax.add_patch(c)
    ax.text(pos['t'][0], pos['t'][1], '汇点\nt', fontsize=16, ha='center',
            va='center', color='white', fontweight='bold', zorder=4, fontproperties=cn_font)

    # ── Legend ──
    legend_elements = [
        mpatches.Patch(color=C_SRC, label='源点 → 比赛 (c = 剩余比赛场次)'),
        mpatches.Patch(color=C_GRAY, label='比赛 → 球队 (c = ∞)'),
        mpatches.Patch(color=C_SINK, label='球队 → 汇点 (c = W_max − wins[i])'),
    ]
    leg = ax.legend(handles=legend_elements, loc='upper right', fontsize=14,
                    framealpha=0.9, bbox_to_anchor=(1.0, 1.02))
    for text in leg.get_texts():
        text.set_fontproperties(cn_font)

    # ── Title ──
    ax.set_title(
        f'流网络结构图 — 判断 {team_name} 是否淘汰\n'
        f'$W_{{max}} = w_{{{team_name}}} + r_{{{team_name}}} = {elim.wins[team_name]} + {elim.remaining[team_name]} = {max_wins}$',
        fontsize=18, fontweight='bold', pad=25, fontproperties=cn_font)

    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-1.5, COL_SINK + 1.5)
    ax.set_ylim(y_min_val - 1.2, y_max_val + 0.8)

    plt.tight_layout(pad=1.0)
    output = f'flow_network_{team_name}.png'
    plt.savefig(output, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"流网络图已保存为 {output}")


def print_detailed_results(results):
    """打印详细求解结果"""
    print("=" * 60)
    print("棒球淘汰问题求解结果")
    print("=" * 60)
    
    for team, info in results.items():
        status = "已淘汰" if info['eliminated'] else "未淘汰"
        print(f"\n{team}:")
        print(f"  当前胜场: {info.get('max_wins', 'N/A')}")
        print(f"  最多可赢: {info['max_wins']} 场")
        print(f"  最大流: {info['flow']}")
        print(f"  总剩余比赛: {info['total_remaining']}")
        print(f"  状态: {status}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("实验六：最大流应用问题 - 棒球淘汰问题")
    print("=" * 60)
    
    # 创建示例
    elim = create_example1()
    
    print("\n球队信息:")
    for team in elim.teams:
        print(f"  {team}: {elim.wins[team]}胜 {elim.losses[team]}负, 剩余{elim.remaining[team]}场")
    
    # 求解
    results = elim.solve_all()
    
    # 打印详细结果
    print_detailed_results(results)
    
    # 可视化结果
    visualize_results(results)
    
    # 可视化被淘汰球队的流网络
    for team, info in results.items():
        if info['eliminated']:
            visualize_flow_network(team, elim)
