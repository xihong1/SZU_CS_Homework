import argparse
import os
import time
from collections import deque
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
import random
import csv
from math import log10


def read_graph_metadata(file_path: str) -> Tuple[int, int]:
    with open(file_path, "r", encoding="utf-8") as f:
        first = f.readline()
        second = f.readline()
        if not first or not second:
            raise ValueError("图文件格式错误：缺少顶点数或边数")
        n = int(first.strip())
        m = int(second.strip())
    return n, m


def edge_iter_from_file(file_path: str) -> Iterable[Tuple[int, int]]:
    with open(file_path, "r", encoding="utf-8") as f:
        _ = f.readline()
        _ = f.readline()
        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v = line.split()
            yield int(u), int(v)


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class DSUJump:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def skip_to_parent(self, x: int, parent: int) -> None:
        self.parent[x] = parent


def load_graph_small(file_path: str) -> Tuple[int, List[Tuple[int, int]], List[List[Tuple[int, int]]]]:
    n, _m = read_graph_metadata(file_path)
    edges: List[Tuple[int, int]] = []
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edge_iter_from_file(file_path)):
        edges.append((u, v))
        adj[u].append((v, edge_id))
        adj[v].append((u, edge_id))
    return n, edges, adj


def baseline_bridge_count(n: int, edges: List[Tuple[int, int]], adj: List[List[Tuple[int, int]]]) -> int:
    bridge_count = 0
    visited = [False] * n

    for edge_id, (u, v) in enumerate(edges):
        for i in range(n):
            visited[i] = False
        queue = deque([u])
        visited[u] = True
        while queue:
            cur = queue.popleft()
            for nxt, eid in adj[cur]:
                if eid == edge_id:
                    continue
                if not visited[nxt]:
                    visited[nxt] = True
                    queue.append(nxt)
        if not visited[v]:
            bridge_count += 1
    return bridge_count


def baseline_bridge_count_from_edges(n: int, edges: List[Tuple[int, int]]) -> int:
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        adj[u].append((v, edge_id))
        adj[v].append((u, edge_id))
    return baseline_bridge_count(n, edges, adj)


def build_spanning_tree(n: int, edge_iter: Iterable[Tuple[int, int]]) -> List[List[int]]:
    dsu = DSU(n)
    tree_adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edge_iter:
        if dsu.union(u, v):
            tree_adj[u].append(v)
            tree_adj[v].append(u)
    return tree_adj


def compute_parent_depth(tree_adj: List[List[int]]) -> Tuple[List[int], List[int]]:
    n = len(tree_adj)
    parent = list(range(n))
    depth = [0] * n
    for start in range(n):
        if parent[start] != start:
            continue
        stack = [start]
        parent[start] = start
        depth[start] = 0
        while stack:
            node = stack.pop()
            for nxt in tree_adj[node]:
                if nxt == parent[node]:
                    continue
                parent[nxt] = node
                depth[nxt] = depth[node] + 1
                stack.append(nxt)
    return parent, depth


def efficient_bridge_count(file_path: str) -> int:
    n, _m = read_graph_metadata(file_path)
    tree_adj = build_spanning_tree(n, edge_iter_from_file(file_path))
    parent, depth = compute_parent_depth(tree_adj)

    marked = [False] * n
    jump = DSUJump(n)

    _n2, _m2 = read_graph_metadata(file_path)
    dsu2 = DSU(n)
    for u, v in edge_iter_from_file(file_path):
        if dsu2.union(u, v):
            continue
        u = jump.find(u)
        v = jump.find(v)
        while u != v:
            if depth[u] < depth[v]:
                u, v = v, u
            if parent[u] == u:
                break
            marked[u] = True
            jump.skip_to_parent(u, parent[u])
            u = jump.find(u)

    bridge_count = 0
    for node in range(n):
        if parent[node] != node and not marked[node]:
            bridge_count += 1
    return bridge_count


def example_graph() -> Tuple[int, List[Tuple[int, int]]]:
    edges = [
        (0, 1), (1, 2), (2, 0),
        (6, 7), (7, 8), (8, 6),
        (2, 3), (3, 4), (4, 5), (5, 6),
        (3, 9), (4, 10),
    ]
    n = 11
    return n, edges


def subexample_graph() -> Tuple[int, List[Tuple[int, int]]]:
    edges = [
        (0, 1),
        (0, 2),
        (2, 3),
    ]
    n = 4
    return n, edges


def efficient_bridge_count_from_edges(n: int, edges: List[Tuple[int, int]]) -> int:
    tree_adj: List[List[int]] = [[] for _ in range(n)]
    dsu = DSU(n)
    for u, v in edges:
        if dsu.union(u, v):
            tree_adj[u].append(v)
            tree_adj[v].append(u)
    parent, depth = compute_parent_depth(tree_adj)
    marked = [False] * n
    jump = DSUJump(n)
    dsu2 = DSU(n)
    for u, v in edges:
        if dsu2.union(u, v):
            continue
        u = jump.find(u)
        v = jump.find(v)
        while u != v:
            if depth[u] < depth[v]:
                u, v = v, u
            if parent[u] == u:
                break
            marked[u] = True
            jump.skip_to_parent(u, parent[u])
            u = jump.find(u)
    bridge_count = 0
    for node in range(n):
        if parent[node] != node and not marked[node]:
            bridge_count += 1
    return bridge_count


def plot_example_graph(output_path: str) -> None:
    n, edges = example_graph()
    bridge_count = efficient_bridge_count_from_edges(n, edges)

    positions = {
        0: (0, 1), 1: (1, 2), 2: (2, 1),
        3: (3, 1), 4: (4, 1), 5: (5, 1),
        6: (6, 1), 7: (7, 2), 8: (8, 1),
        9: (3, 0), 10: (4, 0),
    }

    def is_bridge(edge: Tuple[int, int]) -> bool:
        u, v = edge
        reduced_edges = [e for e in edges if e != edge and e != (v, u)]
        return efficient_bridge_count_from_edges(n, reduced_edges) == bridge_count - 1

    bridge_edges = set()
    for e in edges:
        if is_bridge(e):
            bridge_edges.add(e)
            bridge_edges.add((e[1], e[0]))

    plt.figure(figsize=(8, 3))
    for u, v in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        color = "red" if (u, v) in bridge_edges else "#666666"
        plt.plot([x1, x2], [y1, y2], color=color, linewidth=2)
    for node in range(n):
        x, y = positions[node]
        plt.scatter([x], [y], s=200, color="#1f77b4")
        plt.text(x, y, str(node), color="white", ha="center", va="center", fontsize=10)
    plt.title("Example graph (bridges in red)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_subexample_graph(output_path: str) -> Tuple[int, int]:
    n, edges = subexample_graph()
    baseline_count = baseline_bridge_count_from_edges(n, edges)
    efficient_count = efficient_bridge_count_from_edges(n, edges)

    positions = {
        0: (0, 1),
        1: (1, 1),
        2: (0, 0),
        3: (1, 0),
    }

    plt.figure(figsize=(3, 2.5))
    for u, v in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        plt.plot([x1, x2], [y1, y2], color="red", linewidth=2)
    for node in range(n):
        x, y = positions[node]
        plt.scatter([x], [y], s=220, color="#1f77b4")
        plt.text(x, y, str(node), color="white", ha="center", va="center", fontsize=10)
    plt.title("Subexample (all edges are bridges)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return baseline_count, efficient_count


def plot_performance(results: List[Tuple[str, float, float]], output_path: str) -> None:
    labels = [r[0] for r in results]
    baseline_times = [r[1] for r in results]
    efficient_times = [r[2] for r in results]

    x = range(len(labels))
    width = 0.35
    plt.figure(figsize=(6, 4))
    plt.bar([i - width / 2 for i in x], baseline_times, width=width, label="Baseline")
    plt.bar([i + width / 2 for i in x], efficient_times, width=width, label="DSU-based")
    plt.ylabel("Time (s)")
    plt.title("Bridge counting performance")
    plt.xticks(list(x), labels)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_medium_time(baseline_time: float, efficient_time: float, output_path: str) -> None:
    labels = ["Baseline", "DSU-based"]
    values = [baseline_time, efficient_time]
    plt.figure(figsize=(4, 3))
    plt.bar(labels, values, color=["#4C72B0", "#55A868"])
    plt.ylabel("Time (s)")
    plt.title("Medium graph runtime")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_large_time(efficient_time: float, output_path: str) -> None:
    labels = ["DSU-based"]
    values = [efficient_time]
    plt.figure(figsize=(3, 3))
    plt.bar(labels, values, color=["#55A868"])
    plt.ylabel("Time (s)")
    plt.title("Large graph runtime (DSU-based)")
    for i, v in enumerate(values):
        plt.text(i, v, f"{v:.3f}s", ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_combined_times(medium_baseline: float, medium_efficient: float, large_efficient: float, output_path: str) -> None:
    labels = ["Baseline (medium)", "DSU (medium)", "DSU (large)"]
    values = [medium_baseline, medium_efficient, large_efficient]
    colors = ["#4C72B0", "#55A868", "#55A868"]
    plt.figure(figsize=(6, 4))
    x = range(len(labels))
    plt.bar(x, values, color=colors)
    for i, v in enumerate(values):
        plt.text(i, v, f"{v:.3f}s", ha='center', va='bottom')
    plt.xticks(x, labels)
    plt.ylabel("Time (s)")
    plt.title("Combined runtime comparison")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def run_medium_experiment(file_path: str) -> Tuple[int, float, float]:
    n, edges, adj = load_graph_small(file_path)
    start = time.perf_counter()
    baseline_count = baseline_bridge_count(n, edges, adj)
    baseline_time = time.perf_counter() - start

    start = time.perf_counter()
    efficient_count = efficient_bridge_count(file_path)
    efficient_time = time.perf_counter() - start

    if baseline_count != efficient_count:
        raise ValueError(f"桥数不一致：基准={baseline_count}, 高效={efficient_count}")
    return baseline_count, baseline_time, efficient_time


def run_large_experiment(file_path: str) -> Tuple[int, float]:
    start = time.perf_counter()
    efficient_count = efficient_bridge_count(file_path)
    efficient_time = time.perf_counter() - start
    return efficient_count, efficient_time


def generate_random_graph_file(path: str, n: int, m: int, seed: int = 0) -> None:
    random.seed(seed)
    edges = set()
    while len(edges) < m:
        u = random.randrange(0, n)
        v = random.randrange(0, n)
        if u == v:
            continue
        a, b = min(u, v), max(u, v)
        edges.add((a, b))
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{n}\n{m}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")


def run_scaling_experiments(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    sizes = [
        (100, 500),
        (250, 1273),
        (500, 3000),
        (1000, 8000),
        (5000, 40000),
    ]
    results = []
    csv_path = os.path.join(output_dir, "scaling_results.csv")
    with open(csv_path, "w", newline='', encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["n", "m", "baseline_time", "dsu_time", "baseline_bridges", "dsu_bridges"])
        for n, m in sizes:
            file_path = os.path.join(output_dir, f"rand_{n}_{m}.txt")
            print(f"generate {file_path} ...")
            generate_random_graph_file(file_path, n, m, seed=n + m)
            # run baseline only for small sizes
            baseline_time = None
            baseline_bridges = None
            if n <= 500 and m <= 10000:
                try:
                    n0, edges, adj = load_graph_small(file_path)
                    start = time.perf_counter()
                    baseline_bridges = baseline_bridge_count(n0, edges, adj)
                    baseline_time = time.perf_counter() - start
                except Exception as e:
                    print("baseline failed:", e)
            # DSU-based
            start = time.perf_counter()
            dsu_bridges = efficient_bridge_count(file_path)
            dsu_time = time.perf_counter() - start
            writer.writerow([n, m, baseline_time if baseline_time is not None else "", dsu_time, baseline_bridges if baseline_bridges is not None else "", dsu_bridges])
            results.append((n, m, baseline_time, dsu_time, baseline_bridges, dsu_bridges))
    # plot results
    plot_scaling_results(results, os.path.join(output_dir, "scaling_plot.png"))
    return csv_path, os.path.join(output_dir, "scaling_plot.png")


def plot_scaling_results(results, output_path: str) -> None:
    ns = [r[0] for r in results]
    baseline_times = [r[2] if r[2] is not None else None for r in results]
    dsu_times = [r[3] for r in results]
    plt.figure(figsize=(7, 4))
    # plot DSU times
    plt.plot(ns, dsu_times, marker='o', label='DSU-based')
    # plot baseline where available
    bs_ns = [ns[i] for i, t in enumerate(baseline_times) if t is not None]
    bs_times = [t for t in baseline_times if t is not None]
    if bs_ns:
        plt.plot(bs_ns, bs_times, marker='o', label='Baseline')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('n (log scale)')
    plt.ylabel('Time (s, log scale)')
    plt.title('Scaling: runtime vs n (log-log)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="无向图桥数实验")
    parser.add_argument("--medium", default="mediumG.txt", help="中等规模图文件路径")
    parser.add_argument("--large", default="largeG.txt", help="大型图文件路径")
    parser.add_argument("--output", default="output", help="输出目录")
    parser.add_argument("--skip-large", action="store_true", help="跳过大型图实验")
    parser.add_argument("--skip-baseline-large", action="store_true", help="仅对大型图跳过基准算法")
    parser.add_argument("--scaling", action="store_true", help="运行规模化随机图实验")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    example_path = f"{args.output}/figure2.png"
    plot_example_graph(example_path)

    subexample_path = f"{args.output}/subexample.png"
    sub_baseline, sub_efficient = plot_subexample_graph(subexample_path)

    results = []
    medium_count, medium_baseline_time, medium_efficient_time = run_medium_experiment(args.medium)
    results.append(("medium", medium_baseline_time, medium_efficient_time))

    large_baseline_time = 0.0
    large_efficient_time = 0.0
    large_count = None
    if not args.skip_large:
        if not args.skip_baseline_large:
            n, edges, adj = load_graph_small(args.large)
            start = time.perf_counter()
            _ = baseline_bridge_count(n, edges, adj)
            large_baseline_time = time.perf_counter() - start
        large_count, large_efficient_time = run_large_experiment(args.large)
        results.append(("large", large_baseline_time, large_efficient_time))

    perf_path = f"{args.output}/performance.png"
    plot_performance(results, perf_path)

    medium_time_path = f"{args.output}/medium_time.png"
    plot_medium_time(medium_baseline_time, medium_efficient_time, medium_time_path)
    large_time_path = None
    combined_path = None

    print("示例图输出:", example_path)
    print("子例图输出:", subexample_path)
    print("性能对比图输出:", perf_path)
    print("medium 运行时间图输出:", medium_time_path)
    if args.scaling:
        csv_path, scaling_plot = run_scaling_experiments(args.output)
        print("scaling csv:", csv_path)
        print("scaling plot:", scaling_plot)
    print("medium 图桥数:", medium_count)
    print("medium 基准算法时间(秒):", round(medium_baseline_time, 6))
    print("medium 高效算法时间(秒):", round(medium_efficient_time, 6))
    print("子例桥数(基准/高效):", sub_baseline, sub_efficient)
    if large_count is not None:
        large_time_path = f"{args.output}/large_time.png"
        plot_large_time(large_efficient_time, large_time_path)
        combined_path = f"{args.output}/combined_times.png"
        plot_combined_times(medium_baseline_time, medium_efficient_time, large_efficient_time, combined_path)
        print("large 图桥数:", large_count)
        print("large 高效算法时间(秒):", round(large_efficient_time, 6))
        print("large 运行时间图输出:", large_time_path)
        print("合并时间对比图输出:", combined_path)


if __name__ == "__main__":
    main()
