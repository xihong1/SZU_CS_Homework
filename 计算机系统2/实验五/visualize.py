import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 图1: 矩阵乘法性能对比 ====================
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 数据
sizes = [100, 500, 1000, 1500, 2000, 2500, 3000]
normal_time = [0.000500, 0.069724, 0.591431, 2.286551, 6.915256, 18.264154, 23.647129]
optimized_time = [0.000389, 0.053138, 0.436813, 1.599425, 4.395266, 7.113231, 12.131381]
speedup = [1.28, 1.31, 1.35, 1.43, 1.57, 2.57, 1.95]

# 左图：执行时间对比
x = np.arange(len(sizes))
width = 0.35

bars1 = ax1.bar(x - width/2, normal_time, width, label='普通算法', color='#E74C3C', alpha=0.8)
bars2 = ax1.bar(x + width/2, optimized_time, width, label='优化算法', color='#2ECC71', alpha=0.8)

ax1.set_xlabel('矩阵大小', fontsize=12)
ax1.set_ylabel('执行时间 (秒)', fontsize=12)
ax1.set_title('矩阵乘法执行时间对比', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(sizes)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 添加数值标签
for bar in bars1:
    height = bar.get_height()
    if height > 0.5:
        ax1.annotate(f'{height:.1f}s',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

for bar in bars2:
    height = bar.get_height()
    if height > 0.5:
        ax1.annotate(f'{height:.1f}s',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

# 右图：加速比
ax2.plot(sizes, speedup, 'o-', color='#3498DB', linewidth=2, markersize=8)
ax2.fill_between(sizes, speedup, alpha=0.2, color='#3498DB')
ax2.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='基准线 (1x)')

for i, (s, sp) in enumerate(zip(sizes, speedup)):
    ax2.annotate(f'{sp}x', (s, sp), textcoords="offset points",
                xytext=(0, 10), ha='center', fontsize=10, fontweight='bold')

ax2.set_xlabel('矩阵大小', fontsize=12)
ax2.set_ylabel('加速比', fontsize=12)
ax2.set_title('优化加速比', fontsize=14, fontweight='bold')
ax2.set_xticks(sizes)
ax2.grid(alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('matrix_benchmark.png', dpi=150, bbox_inches='tight')
print("Saved: matrix_benchmark.png")

# ==================== 图2: Cache层次结构分析 ====================
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 5))

# Cache层次结构数据
cache_sizes = [4, 8, 16, 32, 48, 64, 96, 128, 192, 256, 384,
               512, 768, 1024, 1536, 2048, 3072, 4096, 6144,
               8192, 12288, 16384, 24576, 32768, 65536, 131072]
cache_latency = [0.91, 1.02, 0.95, 0.99, 0.93, 0.92, 0.92, 0.94, 0.93, 0.92,
                 0.96, 1.05, 0.99, 1.34, 1.55, 1.59, 1.86, 1.65, 1.76,
                 1.85, 1.78, 3.31, 7.10, 11.81, 12.30, 12.49]

# 左图：Cache延迟曲线
ax3.plot(cache_sizes, cache_latency, 'o-', color='#E67E22', linewidth=2, markersize=5)

# 标记缓存级别区域
ax3.axvspan(0, 768, alpha=0.15, color='green', label='L1 Cache (32KB/核)')
ax3.axvspan(1024, 12288, alpha=0.15, color='blue', label='L2 Cache (1MB/核)')
ax3.axvspan(16384, 24576, alpha=0.15, color='orange', label='L3 Cache (32MB/CCD)')
ax3.axvspan(32768, 131072, alpha=0.15, color='red', label='DRAM (主存)')

# 添加跳变标注
ax3.annotate('L1→L2 跳变\n(~1MB)', xy=(1024, 1.34), xytext=(2000, 2.5),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=10, ha='center', fontweight='bold')

ax3.annotate('L2→L3 跳变\n(~16MB)', xy=(16384, 3.31), xytext=(20000, 5.5),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=10, ha='center', fontweight='bold')

ax3.annotate('L3→DRAM 跳变\n(~32MB)', xy=(32768, 11.81), xytext=(45000, 10),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=10, ha='center', fontweight='bold')

ax3.set_xscale('log', base=2)
ax3.set_xlabel('数组大小 (KB)', fontsize=12)
ax3.set_ylabel('每次访问延迟 (ns)', fontsize=12)
ax3.set_title('Cache层次结构检测（随机访问）', fontsize=14, fontweight='bold')
ax3.legend(loc='upper left', fontsize=9)
ax3.grid(alpha=0.3)
ax3.set_xlim(2, 300000)

# 右图：带宽分析
bandwidth = [78.98, 77.46, 78.65, 75.54, 79.04, 79.36, 76.98, 78.55, 77.52, 77.50,
             77.82, 77.44, 76.30, 76.73, 74.63, 77.86, 78.17, 78.30, 78.16,
             78.53, 78.23, 78.48, 77.64, 77.08, 76.10, 76.67]
bandwidth_sizes = cache_sizes[:len(bandwidth)]

ax4.plot(bandwidth_sizes, bandwidth, 's-', color='#9B59B6', linewidth=2, markersize=5)
ax4.axhline(y=77, color='red', linestyle='--', alpha=0.5, label='平均带宽 ~77 GB/s')

ax4.set_xscale('log', base=2)
ax4.set_xlabel('数组大小 (KB)', fontsize=12)
ax4.set_ylabel('带宽 (GB/s)', fontsize=12)
ax4.set_title('内存带宽测试', fontsize=14, fontweight='bold')
ax4.legend()
ax4.grid(alpha=0.3)
ax4.set_ylim(70, 85)

plt.tight_layout()
plt.savefig('cache_hierarchy.png', dpi=150, bbox_inches='tight')
print("Saved: cache_hierarchy.png")

# ==================== 图3: Cache Line和TLB ====================
fig3, (ax5, ax6) = plt.subplots(1, 2, figsize=(14, 5))

# Cache Line步长测试
stride_sizes = [16, 32, 48, 64, 80, 96, 128, 256, 512, 1024, 2048, 4096]
stride_time = [0.030789, 0.015486, 0.010740, 0.008139, 0.006508, 0.005442,
               0.004080, 0.002061, 0.001042, 0.000512, 0.000294, 0.000336]
# 归一化时间（每次有效访问）
norm_time = [t * 10000 * (64*1024/s) / (64*1024) for t, s in zip(stride_time, stride_sizes)]

ax5.bar(range(len(stride_sizes)), stride_time, color='#1ABC9C', alpha=0.8)
ax5.set_xticks(range(len(stride_sizes)))
ax5.set_xticklabels(stride_sizes, rotation=45)
ax5.set_xlabel('步长 (字节)', fontsize=12)
ax5.set_ylabel('执行时间 (秒)', fontsize=12)
ax5.set_title('Cache Line大小检测（步长测试）', fontsize=14, fontweight='bold')
ax5.grid(axis='y', alpha=0.3)

# 标记64字节边界
ax5.axvline(x=3, color='red', linestyle='--', linewidth=2, label='64字节 (Cache Line)')
ax5.legend()

# 在柱子上添加数值
for i, v in enumerate(stride_time):
    if v > 0.005:
        ax5.text(i, v + 0.0005, f'{v*1000:.1f}ms', ha='center', fontsize=8)

# TLB测试
tlb_pages = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
tlb_sizes_kb = [p * 4 for p in tlb_pages]
tlb_time = [0.000001, 0.000002, 0.000003, 0.000010, 0.000028, 0.000077,
            0.000154, 0.000310, 0.000616, 0.001235, 0.002565, 0.005611,
            0.011310, 0.022613]

ax6.plot(tlb_sizes_kb, tlb_time, 'D-', color='#E74C3C', linewidth=2, markersize=6)
ax6.fill_between(tlb_sizes_kb, tlb_time, alpha=0.2, color='#E74C3C')

ax6.set_xscale('log', base=2)
ax6.set_yscale('log')
ax6.set_xlabel('测试范围 (KB)', fontsize=12)
ax6.set_ylabel('执行时间 (秒, log)', fontsize=12)
ax6.set_title('TLB测量结果', fontsize=14, fontweight='bold')
ax6.grid(alpha=0.3, which='both')

# 标注关键点
ax6.annotate('L1 dTLB: 64条目\n(256KB)', xy=(256, 0.000154), xytext=(512, 0.00005),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=9, ha='center')
ax6.annotate('L2 TLB: 2048条目\n(8MB)', xy=(8192, 0.005611), xytext=(4096, 0.015),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=9, ha='center')

plt.tight_layout()
plt.savefig('cache_line_tlb.png', dpi=150, bbox_inches='tight')
print("Saved: cache_line_tlb.png")

# ==================== 图4: 综合性能分析 ====================
fig4, ax7 = plt.subplots(figsize=(10, 6))

# 不同矩阵大小下两种算法的时间对比（对数坐标）
ax7.semilogy(sizes, normal_time, 'o-', color='#E74C3C', linewidth=2, markersize=8, label='普通算法 (i-j-k)')
ax7.semilogy(sizes, optimized_time, 's-', color='#2ECC71', linewidth=2, markersize=8, label='优化算法 (分块Tiling)')

# 标记数据点
for s, nt, ot in zip(sizes, normal_time, optimized_time):
    ax7.annotate(f'{nt:.2f}s', (s, nt), textcoords="offset points",
                xytext=(0, 10), ha='center', fontsize=8, color='#E74C3C')
    ax7.annotate(f'{ot:.2f}s', (s, ot), textcoords="offset points",
                xytext=(0, -15), ha='center', fontsize=8, color='#2ECC71')

# 标注加速比
for s, sp in zip(sizes, speedup):
    ax7.annotate(f'{sp}x', (s, (normal_time[sizes.index(s)] + optimized_time[sizes.index(s)]) / 2),
                fontsize=10, fontweight='bold', color='blue',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax7.set_xlabel('矩阵大小', fontsize=12)
ax7.set_ylabel('执行时间 (秒, 对数坐标)', fontsize=12)
ax7.set_title('矩阵乘法性能对比（对数坐标）', fontsize=14, fontweight='bold')
ax7.set_xticks(sizes)
ax7.legend(fontsize=11)
ax7.grid(alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('performance_log.png', dpi=150, bbox_inches='tight')
print("Saved: performance_log.png")

print("所有图表已生成：")
print("1. matrix_benchmark.png - 矩阵乘法性能对比")
print("2. cache_hierarchy.png - Cache层次结构分析")
print("3. cache_line_tlb.png - Cache Line和TLB检测")
print("4. performance_log.png - 综合性能分析（对数坐标）")