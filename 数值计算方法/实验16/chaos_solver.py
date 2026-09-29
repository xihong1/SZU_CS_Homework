#!/usr/bin/env python3
"""
实验16：典型混沌系统方程求解
数值计算方法：Euler法、改进Euler法、四阶Runge-Kutta法
系统：Lorenz、Chen、Lü、Chua电路
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import time
import os

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# ==================== 数值方法实现 ====================

def euler_method(f, t_span, y0, h):
    """
    Euler方法（一阶精度）
    f: dy/dt = f(t, y)
    """
    t0, tf = t_span
    n_steps = int((tf - t0) / h)
    t = np.linspace(t0, tf, n_steps + 1)
    y = np.zeros((n_steps + 1, len(y0)))
    y[0] = y0
    for i in range(n_steps):
        y[i+1] = y[i] + h * f(t[i], y[i])
    return t, y

def improved_euler_method(f, t_span, y0, h):
    """
    改进Euler方法（预估-校正法，二阶精度）
    """
    t0, tf = t_span
    n_steps = int((tf - t0) / h)
    t = np.linspace(t0, tf, n_steps + 1)
    y = np.zeros((n_steps + 1, len(y0)))
    y[0] = y0
    for i in range(n_steps):
        y_pred = y[i] + h * f(t[i], y[i])
        y[i+1] = y[i] + h/2 * (f(t[i], y[i]) + f(t[i+1], y_pred))
    return t, y

def rk4_method(f, t_span, y0, h):
    """
    四阶Runge-Kutta方法（四阶精度）
    """
    t0, tf = t_span
    n_steps = int((tf - t0) / h)
    t = np.linspace(t0, tf, n_steps + 1)
    y = np.zeros((n_steps + 1, len(y0)))
    y[0] = y0
    for i in range(n_steps):
        ti, yi = t[i], y[i]
        k1 = f(ti, yi)
        k2 = f(ti + h/2, yi + h/2 * k1)
        k3 = f(ti + h/2, yi + h/2 * k2)
        k4 = f(ti + h, yi + h * k3)
        y[i+1] = yi + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    return t, y

# ==================== 混沌系统定义 ====================

def lorenz_system(t, y, sigma=10.0, rho=28.0, beta=8.0/3.0):
    """Lorenz系统"""
    x, y1, z = y
    dx = sigma * (y1 - x)
    dy = rho * x - x * z - y1
    dz = x * y1 - beta * z
    return np.array([dx, dy, dz])

def chen_system(t, y, a=35.0, b=3.0, c=28.0):
    """Chen系统"""
    x, y1, z = y
    dx = a * (y1 - x)
    dy = (c - a) * x - x * z + c * y1
    dz = x * y1 - b * z
    return np.array([dx, dy, dz])

def lu_system(t, y, a=36.0, b=3.0, c=20.0):
    """Lü系统"""
    x, y1, z = y
    dx = a * (y1 - x)
    dy = -x * z + c * y1
    dz = x * y1 - b * z
    return np.array([dx, dy, dz])

def chua_system(t, y, alpha=9.0, beta=100.0/7.0, m0=-5.0/7.0, m1=-3.0/14.0):
    """Chua电路系统"""
    x, y1, z = y
    # Chua二极管特性函数 f(x) = m1*x + 0.5*(m0-m1)*(|x+1| - |x-1|)
    fx = m1 * x + 0.5 * (m0 - m1) * (abs(x + 1) - abs(x - 1))
    dx = alpha * (y1 - x - fx)
    dy = x - y1 + z
    dz = -beta * y1
    return np.array([dx, dy, dz])

# ==================== 测试验证 ====================

def linear_test_system(t, y):
    """简单线性测试系统 dy/dt = -2y, y(0)=1, 精确解 y=exp(-2t)"""
    return -2 * y

def exact_linear_solution(t):
    """线性测试系统的精确解"""
    return np.exp(-2 * t)

def validate_methods():
    """使用简单算例验证各方法的正确性"""
    print("="*60)
    print("测试验证：dy/dt = -2y, y(0) = 1, t∈[0, 2]")
    print("精确解: y(t) = exp(-2t)")
    print("="*60)

    t_span = (0, 2)
    y0 = np.array([1.0])
    h_list = [0.2, 0.1, 0.05, 0.025]
    exact_final = exact_linear_solution(2.0)

    results = {'Euler': {}, '改进Euler': {}, 'RK4': {}}
    methods = [
        ('Euler', euler_method),
        ('改进Euler', improved_euler_method),
        ('RK4', rk4_method),
    ]

    for name, method in methods:
        print(f"\n{name}方法:")
        for h in h_list:
            t, y = method(linear_test_system, t_span, y0, h)
            y_final = y[-1, 0]
            error = abs(y_final - exact_final)
            results[name][h] = {'final': y_final, 'error': error}
            print(f"  h={h:.3f}: y(2)={y_final:.10f}, 误差={error:.2e}")

    # 生成收敛曲线
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for name, _ in methods:
        hs = sorted(results[name].keys())
        errors = [results[name][h]['error'] for h in hs]
        ax1.loglog(hs, errors, 'o-', linewidth=2, markersize=6, label=name)

    # 理论收敛阶参考线
    ax1.loglog(h_list, [h**1 for h in h_list], 'k--', alpha=0.5, label='O(h) 参考')
    ax1.loglog(h_list, [h**2 for h in h_list], 'k-.', alpha=0.5, label='O(h²) 参考')
    ax1.loglog(h_list, [h**4 for h in h_list], 'k:', alpha=0.5, label='O(h⁴) 参考')

    ax1.set_xlabel('步长 h', fontsize=12)
    ax1.set_ylabel('终点误差', fontsize=12)
    ax1.set_title('数值方法收敛性验证', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # 各方法数值解与精确解对比
    h_plot = 0.05
    t_exact = np.linspace(0, 2, 200)
    y_exact = exact_linear_solution(t_exact)
    ax2.plot(t_exact, y_exact, 'k-', linewidth=2, label='精确解')

    for name, method in methods:
        t, y = method(linear_test_system, t_span, y0, h_plot)
        ax2.plot(t, y[:, 0], 'o--', markersize=3, alpha=0.7, label=name)

    ax2.set_xlabel('t', fontsize=12)
    ax2.set_ylabel('y(t)', fontsize=12)
    ax2.set_title(f'各方法数值解与精确解对比 (h={h_plot})', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    fig.savefig('figures/convergence_validation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n验证图已保存: figures/convergence_validation.png")

    return results

# ==================== 混沌系统求解与可视化 ====================

SYSTEMS = [
    ('Lorenz', lorenz_system, [0.0, 1.0, 0.0], (0, 50), 0.005),
    ('Chen', chen_system, [0.0, 1.0, 0.0], (0, 50), 0.005),
    ('Lu', lu_system, [0.0, 1.0, 0.0], (0, 50), 0.005),
    ('Chua', chua_system, [0.0, 0.5, 0.0], (0, 100), 0.01),
]

def solve_chaos_system(name, f, y0, t_span, h_ref, method='RK4'):
    """求解混沌系统"""
    methods_dict = {
        'Euler': euler_method,
        '改进Euler': improved_euler_method,
        'RK4': rk4_method,
    }
    solver = methods_dict[method]
    start_time = time.time()
    t, y = solver(f, t_span, np.array(y0), h_ref)
    elapsed = time.time() - start_time
    return t, y, elapsed, len(t) - 1

def plot_phase_space_3d(name, t, y, method_name):
    """绘制三维相空间轨迹"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 使用颜色映射显示时间演化
    n_pts = len(t)
    colors = plt.cm.viridis(np.linspace(0, 1, n_pts))

    for i in range(n_pts - 1):
        ax.plot(y[i:i+2, 0], y[i:i+2, 1], y[i:i+2, 2],
                color=colors[i], linewidth=0.3, alpha=0.8)

    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title(f'{name}系统 三维相空间轨迹 ({method_name})', fontsize=14)

    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    fig.savefig(f'figures/{name}_phase3d_{method_name}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: figures/{name}_phase3d_{method_name}.png")

def plot_phase_projections(name, t, y, method_name):
    """绘制二维相平面投影"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    projections = [('X-Y 平面', 0, 1), ('X-Z 平面', 0, 2), ('Y-Z 平面', 1, 2)]

    for ax, (title, i, j) in zip(axes, projections):
        n_pts = len(t)
        colors = plt.cm.viridis(np.linspace(0, 1, n_pts))
        for k in range(n_pts - 1):
            ax.plot(y[k:k+2, i], y[k:k+2, j], color=colors[k], linewidth=0.3, alpha=0.8)
        ax.set_xlabel(['X', 'Y', 'Z'][i], fontsize=10)
        ax.set_ylabel(['X', 'Y', 'Z'][j], fontsize=10)
        ax.set_title(title, fontsize=12)
        ax.grid(True, alpha=0.3)

    fig.suptitle(f'{name}系统 二维相平面投影 ({method_name})', fontsize=14)
    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    fig.savefig(f'figures/{name}_projections_{method_name}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: figures/{name}_projections_{method_name}.png")

def plot_time_series(name, t, y, method_name, max_pts=2000):
    """绘制时间序列图"""
    # 降采样
    step = max(1, len(t) // max_pts)
    t_plot = t[::step]
    y_plot = y[::step]

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    for i, ax in enumerate(axes):
        ax.plot(t_plot, y_plot[:, i], linewidth=0.5, color=['#2196F3', '#FF5722', '#4CAF50'][i])
        ax.set_ylabel(['X(t)', 'Y(t)', 'Z(t)'][i], fontsize=10)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel('时间 t', fontsize=12)
    fig.suptitle(f'{name}系统 时间序列 ({method_name})', fontsize=14)
    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    fig.savefig(f'figures/{name}_timeseries_{method_name}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: figures/{name}_timeseries_{method_name}.png")

def compare_methods_one_system(name, f, y0, t_span, h):
    """对比三种方法在同一个系统上的表现"""
    fig = plt.figure(figsize=(18, 12))

    methods_list = [('Euler', euler_method), ('改进Euler', improved_euler_method), ('RK4', rk4_method)]

    for idx, (mname, method) in enumerate(methods_list):
        t, y = method(f, t_span, np.array(y0), h)

        # 3D相空间
        ax = fig.add_subplot(2, 3, idx + 1, projection='3d')
        n_pts = len(t)
        colors = plt.cm.viridis(np.linspace(0, 1, n_pts))
        for i in range(n_pts - 1):
            ax.plot(y[i:i+2, 0], y[i:i+2, 1], y[i:i+2, 2],
                    color=colors[i], linewidth=0.3, alpha=0.8)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{mname}', fontsize=12)

        # 时间序列
        ax2 = fig.add_subplot(2, 3, idx + 4)
        step = max(1, len(t) // 1500)
        t_plot = t[::step]
        y_plot = y[::step]
        ax2.plot(t_plot, y_plot[:, 0], linewidth=0.5, label='X(t)', alpha=0.7)
        ax2.plot(t_plot, y_plot[:, 1], linewidth=0.5, label='Y(t)', alpha=0.7)
        ax2.plot(t_plot, y_plot[:, 2], linewidth=0.5, label='Z(t)', alpha=0.7)
        ax2.set_xlabel('t')
        ax2.set_ylabel('值')
        ax2.set_title(f'{mname} - 时间序列')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

    fig.suptitle(f'{name}系统 - 三种数值方法对比 (h={h})', fontsize=16, fontweight='bold')
    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    fig.savefig(f'figures/{name}_methods_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: figures/{name}_methods_comparison.png")

def plot_sensitivity_analysis(name, f, t_span, h=0.005):
    """初值敏感性分析（蝴蝶效应验证）"""
    y0_base = [0.0, 1.0, 0.0] if name != 'Chua' else [0.0, 0.5, 0.0]

    # 三个微小不同的初值
    deltas = [0.0, 1e-6, 1e-4]

    fig, axes = plt.subplots(3, 1, figsize=(12, 8))

    for delta in deltas:
        y0 = [y0_base[0] + delta, y0_base[1], y0_base[2]]
        t, y = rk4_method(f, t_span, np.array(y0), h)
        label = f'初值偏移 δ={delta:.0e}'
        axes[0].plot(t, y[:, 0], linewidth=0.5, alpha=0.8, label=label)
        axes[1].plot(t, y[:, 1], linewidth=0.5, alpha=0.8, label=label)
        axes[2].plot(t, y[:, 2], linewidth=0.5, alpha=0.8, label=label)

    for i, ax in enumerate(axes):
        ax.set_ylabel(['X(t)', 'Y(t)', 'Z(t)'][i], fontsize=10)
        ax.grid(True, alpha=0.3)
        if i == 0:
            ax.legend(fontsize=8)

    axes[-1].set_xlabel('时间 t', fontsize=12)
    fig.suptitle(f'{name}系统 - 初值敏感性分析（蝴蝶效应验证）', fontsize=14)
    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    fig.savefig(f'figures/{name}_sensitivity.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: figures/{name}_sensitivity.png")

def compute_lyapunov_approx(name, f, y0, t_span, h=0.005, delta=1e-8):
    """使用参考轨迹偏差法近似计算最大Lyapunov指数

    基于两个邻近轨迹的发散率来估计
    """
    # 参考轨迹
    t, y_ref = rk4_method(f, t_span, np.array(y0), h)

    # 扰动轨迹
    y0_pert = np.array([y0[0] + delta, y0[1], y0[2]])
    t, y_pert = rk4_method(f, t_span, y0_pert, h)

    # 计算对数发散率
    n = len(t)
    d = np.zeros(n)
    for i in range(n):
        d[i] = np.linalg.norm(y_pert[i] - y_ref[i])

    # 避免log(0)
    d = np.maximum(d, 1e-15)
    log_d = np.log(d)

    # 线性拟合斜率即为最大Lyapunov指数
    # 使用后半段数据（排除暂态）
    n_half = n // 2
    t_fit = t[n_half:]
    log_d_fit = log_d[n_half:]

    # 简单线性回归
    t_mean = np.mean(t_fit)
    d_mean = np.mean(log_d_fit)
    slope = np.sum((t_fit - t_mean) * (log_d_fit - d_mean)) / np.sum((t_fit - t_mean)**2)

    return slope, t, d

def main():
    """主函数"""
    print("=" * 70)
    print("实验16：典型混沌系统方程求解")
    print("=" * 70)

    # Step 1: 方法验证
    print("\n>>> Step 1: 方法正确性验证")
    validate_methods()

    # Step 2: 求解混沌系统
    print("\n>>> Step 2: 求解各混沌系统")

    all_results = {}

    for name, f, y0, t_span, h in SYSTEMS:
        print(f"\n--- {name}系统 ---")
        print(f"  初始条件: {y0}")
        print(f"  时间区间: [{t_span[0]}, {t_span[1]}]")
        print(f"  步长: h = {h}")

        system_results = {}

        for method_name in ['Euler', '改进Euler', 'RK4']:
            t, y, elapsed, n_steps = solve_chaos_system(name, f, y0, t_span, h, method_name)
            system_results[method_name] = {
                't': t, 'y': y, 'time': elapsed, 'n_steps': n_steps
            }
            print(f"  {method_name}: {n_steps}步, 耗时 {elapsed:.4f}s")

            # 生成图表
            plot_phase_space_3d(name, t, y, method_name)
            if method_name == 'RK4':  # 只为最优方法生成详细图
                plot_phase_projections(name, t, y, method_name)
                plot_time_series(name, t, y, method_name)

        # 方法对比图
        compare_methods_one_system(name, f, y0, t_span, h)

        # 初值敏感性分析
        plot_sensitivity_analysis(name, f, t_span, h)

        # 近似Lyapunov指数
        lyap, t_lyap, d_lyap = compute_lyapunov_approx(name, f, y0, t_span, h)
        print(f"  近似最大Lyapunov指数: {lyap:.6f}")
        system_results['lyapunov'] = lyap

        all_results[name] = system_results

    # Step 3: 方法精度对比
    print("\n>>> Step 3: 方法精度对比分析")

    # 以RK4在极小步长下的解作为参考，计算各方法的全局误差
    for name, f, y0, t_span, h in SYSTEMS:
        print(f"\n--- {name}系统 精度对比 ---")

        # 参考解（RK4，更小步长）
        h_ref = h / 4
        t_ref, y_ref = rk4_method(f, t_span, np.array(y0), h_ref)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        for method_name in ['Euler', '改进Euler', 'RK4']:
            result = all_results[name][method_name]
            t = result['t']
            y = result['y']

            # 插值到相同时间点计算误差
            y_interp = np.zeros_like(y_ref)
            for dim in range(3):
                y_interp[:, dim] = np.interp(t_ref, t, y[:, dim])

            error = np.sqrt(np.sum((y_interp - y_ref)**2, axis=1))

            ax = axes[0]
            ax.semilogy(t_ref, error, linewidth=1, alpha=0.8, label=method_name)

            # 终点误差
            y_final_interp = np.array([np.interp(t_span[1], t, y[:, d]) for d in range(3)])
            y_ref_final = y_ref[-1]
            final_error = np.linalg.norm(y_final_interp - y_ref_final)
            print(f"  {method_name}: 终点误差 = {final_error:.6e}")

        axes[0].set_xlabel('时间 t', fontsize=12)
        axes[0].set_ylabel('全局误差 (2-范数)', fontsize=12)
        axes[0].set_title(f'{name}系统 - 误差演化曲线', fontsize=13)
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)

        # 相空间轨迹对比（只用RK4的精细步长）
        ax = axes[1]
        ax = fig.add_subplot(1, 2, 2, projection='3d')
        ax.plot(y_ref[:, 0], y_ref[:, 1], y_ref[:, 2],
                linewidth=0.3, color='blue', alpha=0.8)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{name}系统 - RK4参考轨迹 (h={h_ref})', fontsize=13)

        plt.tight_layout()
        fig.savefig(f'figures/{name}_error_analysis.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  已保存: figures/{name}_error_analysis.png")

    # Step 4: 汇总对比图 - 所有系统3D吸引子
    print("\n>>> Step 4: 生成汇总图表")

    fig = plt.figure(figsize=(16, 14))
    for idx, (name, f, y0, t_span, h) in enumerate(SYSTEMS):
        t, y = rk4_method(f, t_span, np.array(y0), h)

        ax = fig.add_subplot(2, 2, idx + 1, projection='3d')
        n_pts = len(t)
        colors = plt.cm.viridis(np.linspace(0, 1, n_pts))
        for i in range(n_pts - 1):
            ax.plot(y[i:i+2, 0], y[i:i+2, 1], y[i:i+2, 2],
                    color=colors[i], linewidth=0.3, alpha=0.8)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{name}系统 混沌吸引子', fontsize=14, fontweight='bold')

    fig.suptitle('四种典型混沌系统的吸引子结构对比 (RK4方法)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    fig.savefig('figures/all_systems_attractors.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  已保存: figures/all_systems_attractors.png")

    # 计算性能对比表
    print("\n>>> Step 5: 性能汇总")
    print("\n" + "="*80)
    print(f"{'系统':<8} {'方法':<10} {'步数':<8} {'计算时间(s)':<14} {'近似Lyapunov指数'}")
    print("-"*80)
    for name in all_results:
        for mname in ['Euler', '改进Euler', 'RK4']:
            r = all_results[name][mname]
            print(f"{name:<8} {mname:<10} {r['n_steps']:<8} {r['time']:<14.4f}", end="")
            if mname == 'RK4':
                print(f" {all_results[name].get('lyapunov', 0):>20.6f}")
            else:
                print()

    print("\n所有图表生成完毕！保存在 figures/ 目录下。")
    return all_results

if __name__ == '__main__':
    results = main()
