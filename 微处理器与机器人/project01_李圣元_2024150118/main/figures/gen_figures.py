# -*- coding: utf-8 -*-
"""
跑马灯实验报告配图生成脚本
运行：python gen_figures.py
输出：../images/*.png

绘图约定：画布统一使用 0~100 的“绘图单位”，figsize 按内容范围等比设置，
使两个方向上的单位长度相等（文字与图形不会被拉伸）；
同时把图片物理尺寸控制在 7 in 左右，这样在 LaTeX 中按 \\linewidth 插入时
缩放比例接近 1，正文字号不会被压得太小。
"""
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
os.makedirs(OUT, exist_ok=True)

# ----------------------------- 配色 -----------------------------
C_BLUE, C_BLUE_F = "#2f5f9e", "#e8f1fb"
C_ORG, C_ORG_F = "#c98a1a", "#fff6e4"
C_GRN, C_GRN_F = "#2f7d4f", "#e9f6ee"
C_RED, C_RED_F = "#b03a3a", "#fdeeee"
C_GRAY, C_GRAY_F = "#4a4a4a", "#f0f0f0"
C_PUR, C_PUR_F = "#6a4fa3", "#f1ecfa"


def canvas(w, h, xlim=(0, 100), ylim=(0, 100)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    return fig, ax


def box(ax, x, y, w, h, text, fc=C_BLUE_F, ec=C_BLUE, fs=10, bold=False,
        rounded=True, ls="-"):
    style = "round,pad=0,rounding_size=1.2" if rounded else "square,pad=0"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec,
                                lw=1.4, zorder=3, linestyle=ls))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, fontweight="bold" if bold else "normal",
                zorder=4, linespacing=1.5, color="#1a1a1a")


def diamond(ax, cx, cy, w, h, text, fc=C_ORG_F, ec=C_ORG, fs=9.5):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.4, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=4,
            linespacing=1.4, color="#1a1a1a")


def arrow(ax, p0, p1, color=C_GRAY, lw=1.4, rad=0.0, style="-|>", ms=10):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0,
                                 connectionstyle="arc3,rad=%s" % rad, zorder=2))


def line(ax, pts, color=C_GRAY, lw=1.4, ls="-"):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw,
            linestyle=ls, zorder=2, solid_capstyle="round")


def tag(ax, x, y, text, fs=9, color="#1a1a1a", ha="center", va="center",
        rot=0, bg=None):
    t = ax.text(x, y, text, fontsize=fs, ha=ha, va=va, color=color, zorder=5,
                linespacing=1.4, rotation=rot)
    if bg:
        t.set_bbox(dict(fc=bg, ec="none", pad=1.5))
    return t


def dot(ax, x, y, r=0.9, color=C_GRAY):
    ax.add_patch(Circle((x, y), r, fc=color, ec="none", zorder=5))


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=220, facecolor="white", bbox_inches="tight",
                pad_inches=0.08)
    plt.close(fig)
    print("saved", name)


# ================================================================
# 1. 系统总体结构框图
# ================================================================
def fig_system():
    fig, ax = canvas(7.0, 6.6, ylim=(6, 100))

    box(ax, 27, 12, 46, 80, "", fc="#f7fafd", ec=C_BLUE, rounded=False)
    tag(ax, 50, 87, "STM32F429IGT6  主控制器", fs=11, color=C_BLUE)

    box(ax, 29, 66, 19, 14, "GPIO 输入\n按键扫描与消抖\nkey_scan( )", fs=8.5)
    box(ax, 52, 66, 19, 14, "GPIO 输出\n灯态掩码刷新\nled_write( )", fs=8.5)
    box(ax, 29, 42, 19, 14, "主循环调度\n计时 / 状态切换\nmain( ) 主循环", fs=8.5)
    box(ax, 52, 42, 19, 14, "软件 I2C 主机\n蜂鸣器驱动\nbeep_start / task", fs=8.5)
    box(ax, 29, 20, 42, 14,
        "灯效算法层\neffect_run( effect, step )\n"
        "单灯流水 / 双灯追逐 / 乒乓往返 / 逐个点亮", fs=8.5,
        fc=C_PUR_F, ec=C_PUR)

    box(ax, 1, 64, 18, 16,
        "4 个独立按键\nKEY0 = PH3\nKEY1 = PH2\nKEY2 = PC13\nKEY3 = PA0",
        fs=7.5, fc=C_GRN_F, ec=C_GRN)
    arrow(ax, (19, 72), (29, 72))
    tag(ax, 24, 84, "按键电平", fs=8, color=C_GRN)

    box(ax, 81, 64, 18, 16,
        "8 路 LED\nPB0 = LED7\nPB3…PB9\n= LED0…LED6\n低电平点亮",
        fs=8, fc=C_RED_F, ec=C_RED)
    arrow(ax, (71, 72), (81, 72))
    tag(ax, 77, 84, "8 位掩码", fs=8, color=C_RED)

    box(ax, 81, 44, 18, 12, "PCF8574\nI2C 扩展芯片\n地址 0x20", fs=8.5,
        fc=C_ORG_F, ec=C_ORG)
    arrow(ax, (71, 49), (81, 49))
    tag(ax, 76, 49, "SCL = PH4   SDA = PH5", fs=7.5, color=C_ORG, rot=90)

    box(ax, 81, 24, 18, 12, "板载蜂鸣器\n( PCF8574 的 P0 脚 )", fs=8.5,
        fc=C_ORG_F, ec=C_ORG)
    arrow(ax, (90, 44), (90, 36))

    tag(ax, 50, 9, "全部外设由主循环统一调度，不使用 HAL_Delay 阻塞，"
                   "按键响应、灯效推进、蜂鸣器计时互不干扰", fs=8.5, color="#555555")
    tag(ax, 1, 97, "系统总体结构框图", fs=12, ha="left")

    save(fig, "fig01_system_block.png")


# ================================================================
# 2. 引脚分配图
# ================================================================
def fig_pinmap():
    fig, ax = canvas(7.0, 6.3, ylim=(10, 100))

    pins = [("PB0", "LED7", 7), ("PB3", "LED0", 0), ("PB4", "LED1", 1),
            ("PB5", "LED2", 2), ("PB6", "LED3", 3), ("PB7", "LED4", 4),
            ("PB8", "LED5", 5), ("PB9", "LED6", 6)]

    box(ax, 8, 8, 26, 80, "", fc="#f2f5f9", ec=C_GRAY, rounded=False)
    tag(ax, 21, 85, "GPIOB 端口", fs=11, color=C_GRAY)

    y0, dy = 78, 8.4
    for i, (pin, led, bit) in enumerate(pins):
        y = y0 - i * dy
        tag(ax, 32.5, y, pin, fs=10, ha="right", color=C_BLUE)
        line(ax, [(34, y), (43, y)], color=C_GRAY, lw=1.6)
        arrow(ax, (43, y), (57, y), color=C_BLUE)
        box(ax, 57, y - 3.1, 22, 6.2, led, fs=10, bold=True,
            fc=C_RED_F, ec=C_RED)
        tag(ax, 81, y, "掩码 bit%d" % bit, fs=9, ha="left", color=C_PUR)

    tag(ax, 1, 97, "8 路 LED 引脚分配", fs=12, ha="left")
    tag(ax, 8, 93, "PB1：板载 DS0 红色指示灯（本实验未使用）；PB2：未分配",
        fs=8.5, ha="left", color="#777777")

    save(fig, "fig02_pin_map.png")


# ================================================================
# 3. LED 驱动电路
# ================================================================
def fig_schematic():
    fig, ax = canvas(7.0, 4.4, ylim=(30, 100))

    y = 74
    line(ax, [(10, y), (18, y)], lw=2.0, color=C_RED)
    line(ax, [(13, y + 4), (13, y)], lw=1.6, color=C_RED)
    tag(ax, 9, y + 5, "+3.3 V", fs=10, ha="left", color=C_RED)

    box(ax, 18, y - 3.2, 12, 6.4, "1 kΩ", fs=10, fc="#ffffff", ec=C_GRAY,
        rounded=False)
    line(ax, [(30, y), (38, y)], lw=1.6)

    ax.add_patch(Polygon([(38, y - 4), (38, y + 4), (46, y)], closed=True,
                         fc="#ffd9d9", ec=C_RED, lw=1.6, zorder=3))
    line(ax, [(46, y - 4.5), (46, y + 4.5)], lw=2.4, color=C_RED)
    line(ax, [(46, y), (55, y)], lw=1.6)

    arrow(ax, (32, y + 10), (44, y + 10), color=C_GRN, lw=1.6)
    tag(ax, 38, y + 13.5, "电流 I", fs=9, color=C_GRN)

    tag(ax, 39, y - 8, "长脚（阳极）", fs=8.5, color="#777777")
    tag(ax, 49, y - 8, "短脚（阴极）", fs=8.5, color="#777777")

    box(ax, 55, y - 7, 20, 14, "GPIOB 引脚\n（如 PB3）", fs=9.5, fc=C_BLUE_F,
        ec=C_BLUE)

    box(ax, 6, 34, 88, 22,
        "IO 输出低电平（0 V）：引脚相当于接地，3.3 V → 电阻 → LED → 引脚 形成回路，LED 点亮\n"
        "IO 输出高电平（3.3 V）：引脚与电源同电位，回路两端没有电压差，LED 熄灭\n"
        "8 路 LED 接法完全相同，只是把“PB3”依次换成 PB4、PB5、PB6、PB7、PB8、PB9、PB0",
        fs=8.5, fc=C_GRN_F, ec=C_GRN)

    tag(ax, 1, 96, "单路 LED 驱动电路（共 8 路，接法相同）", fs=12, ha="left")

    save(fig, "fig03_led_schematic.png")


# ================================================================
# 4. 主程序流程图
# ================================================================
def fig_main_flow():
    fig, ax = canvas(5.9, 9.0, xlim=(0, 100), ylim=(0, 152))
    cx = 34

    def go(a, b, color=C_GRAY):
        arrow(ax, a, b, color=color)

    box(ax, cx - 10, 141, 20, 8, "开始", fs=11, fc=C_GRN_F, ec=C_GRN, bold=True)
    go((cx, 141), (cx, 136))

    box(ax, cx - 24, 126, 48, 10,
        "系统初始化\nHAL_Init( )；SystemClock_Config( )；MX_GPIO_Init( )", fs=9)
    go((cx, 126), (cx, 121))

    box(ax, cx - 24, 111, 48, 10,
        "外设初始化\nled_init( )；key_init( )；beep_init( )", fs=9)
    go((cx, 111), (cx, 106))

    box(ax, cx - 24, 96, 48, 10,
        "显示初始灯效\neffect_run(cur_effect, 0)；effect_tick = HAL_GetTick( )", fs=9)
    go((cx, 96), (cx, 91))

    dot(ax, cx, 89)
    tag(ax, cx - 2, 93, "主循环入口", fs=8.5, ha="right", color=C_PUR)

    box(ax, cx - 24, 78, 48, 10, "扫描按键\nkey = key_scan( )", fs=9)
    go((cx, 78), (cx, 73))

    diamond(ax, cx, 63, 30, 16, "key ≠ 0 ？", fs=10)
    go((cx, 55), (cx, 46))
    tag(ax, cx + 17, 66, "是", fs=9, color=C_GRN)
    tag(ax, cx + 17, 59, "否", fs=9, color=C_GRAY)

    line(ax, [(cx + 15, 63), (cx + 24, 63)], color=C_GRN)
    go((cx + 24, 62), (cx + 24, 41), color=C_GRN)
    box(ax, cx + 24, 51, 40, 22,
        "切换到第 key 种灯效\ncur_effect = key − 1\neffect_step = 0\n"
        "effect_tick = HAL_GetTick( )\nbeep_start(80)\n// 蜂鸣器只响一声",
        fs=8.5, fc=C_GRN_F, ec=C_GRN)
    line(ax, [(cx + 44, 51), (cx + 44, 46)], color=C_GRN)
    line(ax, [(cx, 46), (cx + 44, 46)], color=C_GRN)
    dot(ax, cx, 46, color=C_GRN)

    diamond(ax, cx, 29, 42, 16,
            "HAL_GetTick( ) − effect_tick\n≥ 灯效间隔时间 ？", fs=8.5)
    go((cx, 21), (cx, 13))
    tag(ax, cx + 24.5, 32, "是", fs=9, color=C_GRN)
    tag(ax, cx + 24.5, 25.5, "否", fs=9, color=C_GRAY)

    line(ax, [(cx + 21, 29), (cx + 24, 29)], color=C_GRN)
    go((cx + 24, 28), (cx + 24, 19), color=C_GRN)
    box(ax, cx + 24, 18, 40, 19,
        "推进到下一步\neffect_tick = HAL_GetTick( )\neffect_step + +\n"
        "effect_run(cur_effect, effect_step)", fs=8.5, fc=C_GRN_F, ec=C_GRN)
    line(ax, [(cx + 44, 18), (cx + 44, 13)], color=C_GRN)
    line(ax, [(cx, 13), (cx + 44, 13)], color=C_GRN)
    dot(ax, cx, 13, color=C_GRN)

    box(ax, cx - 24, 3, 48, 10, "蜂鸣器计时处理\nbeep_task( )", fs=9)
    go((cx, 13), (cx, 8))

    line(ax, [(cx - 24, 8), (cx - 29, 8)], color=C_PUR)
    line(ax, [(cx - 29, 8), (cx - 29, 89)], color=C_PUR)
    go((cx - 29, 89), (cx - 3, 89), color=C_PUR)
    tag(ax, cx - 28, 93, "返回主循环", fs=8.5, ha="left", color=C_PUR)

    tag(ax, 1, 148, "主程序流程图", fs=12, ha="left")

    save(fig, "fig04_main_flow.png")


# ================================================================
# 5. 按键扫描流程图
# ================================================================
def fig_key_flow():
    fig, ax = canvas(5.9, 7.5, xlim=(0, 100), ylim=(4, 130))
    cx = 38

    def go(a, b, color=C_GRAY):
        arrow(ax, a, b, color=color)

    box(ax, cx - 20, 118, 40, 9, "进入 key_scan( )", fs=11, fc=C_GRN_F,
        ec=C_GRN, bold=True)
    go((cx, 118), (cx, 113))

    box(ax, cx - 24, 103, 48, 10, "i = 0；ret = 0\nnow = HAL_GetTick( )", fs=9)
    go((cx, 103), (cx, 98))

    diamond(ax, cx, 90, 26, 15, "i < 4 ？", fs=10)
    go((cx, 82.5), (cx, 77))
    tag(ax, cx + 13, 84, "是", fs=9, ha="left", color=C_GRN)
    line(ax, [(cx + 13, 90), (cx + 22, 90)], color=C_RED)
    go((cx + 22, 90), (cx + 28, 90), color=C_RED)
    box(ax, cx + 28, 85, 32, 10, "返回 ret", fs=10, fc=C_GRN_F, ec=C_GRN)
    tag(ax, cx + 15.5, 93.5, "否", fs=9, ha="left", color=C_RED)

    box(ax, cx - 28, 68, 56, 9,
        "raw = 读取第 i 个按键电平（高有效按键取反，统一 1 = 按下）", fs=8.5)
    go((cx, 68), (cx, 63))

    diamond(ax, cx, 54, 44, 16, "raw ≠ last_raw[i] ？", fs=9)
    go((cx, 46), (cx, 42))
    tag(ax, cx + 3, 44, "否", fs=9, ha="left", color=C_GRAY)
    line(ax, [(cx + 22, 54), (cx + 30, 54)], color=C_GRN)
    go((cx + 30, 54), (cx + 36, 54), color=C_GRN)
    tag(ax, cx + 26, 57, "是", fs=9, color=C_GRN)
    box(ax, cx + 36, 46, 30, 16,
        "重新开始计时\nlast_raw[i] = raw\nchange_tick[i] = now", fs=8.5,
        fc=C_GRN_F, ec=C_GRN)
    line(ax, [(cx + 51, 46), (cx + 51, 42)], color=C_GRN)
    line(ax, [(cx, 42), (cx + 51, 42)], color=C_GRN)
    dot(ax, cx, 42, color=C_GRN)

    diamond(ax, cx, 29, 62, 17,
            "now − change_tick[i] ≥ 10 ms\n且 raw ≠ stable[i] ？", fs=8.5)
    go((cx, 20.5), (cx, 15))
    tag(ax, cx + 3, 17, "否", fs=9, ha="left", color=C_GRAY)
    line(ax, [(cx + 31, 29), (cx + 37, 29)], color=C_GRN)
    go((cx + 37, 29), (cx + 43, 29), color=C_GRN)
    tag(ax, cx + 34, 32, "是", fs=9, color=C_GRN)
    box(ax, cx + 43, 20, 25, 18,
        "stable[i] = raw\n\n若 raw == 1（按下）\n则 ret = i + 1\n\n按住不放不重复触发",
        fs=8, fc=C_GRN_F, ec=C_GRN)
    line(ax, [(cx + 55.5, 20), (cx + 55.5, 15)], color=C_GRN)
    line(ax, [(cx, 15), (cx + 55.5, 15)], color=C_GRN)
    dot(ax, cx, 15, color=C_GRN)

    box(ax, cx - 15, 6, 30, 9, "i + +", fs=10)

    line(ax, [(cx - 15, 10.5), (cx - 22, 10.5)], color=C_PUR)
    line(ax, [(cx - 22, 10.5), (cx - 22, 92)], color=C_PUR)
    go((cx - 22, 92), (cx - 13, 92), color=C_PUR)

    tag(ax, 1, 127, "按键扫描与消抖流程图", fs=12, ha="left")

    save(fig, "fig05_key_flow.png")


# ================================================================
# 6. 按键抖动与消抖时序
# ================================================================
def fig_debounce():
    fig, axes = plt.subplots(3, 1, figsize=(7.6, 4.6), sharex=True)
    fig.subplots_adjust(left=0.135, right=0.985, top=0.88, bottom=0.14,
                        hspace=0.32)

    press, release = 20, 70
    bounce = [(20.0, 21.0), (21.6, 22.4), (22.9, 23.4), (24.2, 24.7),
              (25.6, 26.1), (27.3, 27.7)]
    bounce_r = [(70.0, 70.5), (71.2, 71.9), (72.6, 73.1), (74.4, 74.9)]

    def style(ax, title, color):
        ax.set_ylim(-0.35, 1.62)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["松开\n(1)", "按下\n(0)"], fontsize=8)
        ax.set_title(title, fontsize=9.5, color=color, pad=5)
        ax.grid(axis="x", ls=":", color="#cccccc")
        ax.axvspan(press, press + 10, color=C_ORG, alpha=0.18)
        ax.axvspan(release, release + 10, color=C_ORG, alpha=0.18)

    ax = axes[0]
    ax.plot([0, press, press, release, release, 100], [1, 1, 0, 0, 1, 1],
            color=C_GRN, lw=2.0)
    style(ax, "(a) 理想按键波形：按下瞬间电平干净地由 1 变 0", C_GRN)
    ax.text(press + 5, 1.38, "10 ms 消抖窗口", fontsize=8, ha="center",
            color=C_ORG)

    ax = axes[1]
    xs, ys = [0], [1]
    for s, e in bounce:
        xs += [s, e]
        ys += [0, 1]
    xs += [press + 10, release]
    ys += [0, 1]
    for s, e in bounce_r:
        xs += [s, e]
        ys += [0, 1]
    xs += [release + 10, 100]
    ys += [1, 1]
    ax.plot(xs, ys, color=C_RED, lw=1.5)
    style(ax, "(b) 实际按键波形：机械触点抖动，电平在数毫秒内反复跳变", C_RED)

    ax = axes[2]
    ax.plot([0, press + 10, release + 10, 100], [0, 1, 0, 0],
            color=C_BLUE, lw=2.0)
    style(ax, "(c) 软件识别出的稳定状态 stable[i]：抖动被完整过滤", C_BLUE)
    ax.annotate("", xy=(press + 10, 1.0), xytext=(press + 10, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=C_PUR, lw=1.4))
    ax.text(press + 12, 1.3, "只在此刻产生一次“按下事件” ret = i + 1",
            fontsize=8, color=C_PUR, va="center")
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 10))
    ax.set_xlabel("时间 / ms", fontsize=9)

    fig.suptitle("按键抖动与软件消抖时序对比", fontsize=11.5, y=0.965)
    save(fig, "fig06_debounce.png")


# ================================================================
# 7. 模块层次与调用关系
# ================================================================
def fig_modules():
    fig, ax = canvas(6.8, 6.2, ylim=(2, 100))

    box(ax, 27, 86, 46, 12, "main.c\nmain( )：初始化 → while(1) 主循环调度",
        fs=9.5, fc=C_PUR_F, ec=C_PUR, bold=True)
    arrow(ax, (42, 86), (16.5, 76), color=C_PUR)
    arrow(ax, (50, 86), (50, 76), color=C_PUR)
    arrow(ax, (58, 86), (83.5, 76), color=C_PUR)

    box(ax, 1, 50, 31, 26,
        "led.c / led.h\n————————\nled_init( )\nled_write( mask )\n"
        "effect_run( )\neffect_interval( )\n端口初始化 / 掩码刷新\n灯效调度 / 间隔时间",
        fs=8, fc=C_RED_F, ec=C_RED)
    box(ax, 34.5, 50, 31, 26,
        "key.c / key.h\n————————\nkey_init( )\nkey_scan( )\n"
        "key_is_pressed( )\n[static 内部函数]\n端口初始化 / 扫描消抖\n"
        "KEY_DEBOUNCE_MS = 10",
        fs=8, fc=C_GRN_F, ec=C_GRN)
    box(ax, 68, 50, 31, 26,
        "beep.c / beep.h\n————————\nbeep_init( )\nbeep_start( ms )\n"
        "beep_task( )\npcf8574_write_bit( )\nI2C 初始化 / 开始鸣响\n"
        "到点自动关闭",
        fs=8, fc=C_ORG_F, ec=C_ORG)

    box(ax, 1, 26, 98, 16,
        "STM32F4xx HAL 库\nHAL_GPIO_Init( )    HAL_GPIO_WritePin( )\n"
        "HAL_GPIO_ReadPin( )    HAL_GetTick( )    __HAL_RCC_GPIOx_CLK_ENABLE( )",
        fs=8, fc=C_BLUE_F, ec=C_BLUE)
    arrow(ax, (16.5, 50), (30, 42), color=C_RED)
    arrow(ax, (50, 50), (50, 42), color=C_GRN)
    arrow(ax, (83.5, 50), (70, 42), color=C_ORG)

    box(ax, 1, 4, 98, 16,
        "硬件层\nGPIOB（8 路 LED）    GPIOH / GPIOC / GPIOA（4 个按键）\n"
        "PH4 / PH5 软件 I2C → PCF8574 → 蜂鸣器",
        fs=8, fc=C_GRAY_F, ec=C_GRAY)
    arrow(ax, (50, 26), (50, 20), color=C_BLUE)

    tag(ax, 1, 97, "软件模块层次与调用关系", fs=12, ha="left")

    save(fig, "fig07_module_tree.png")


# ================================================================
# 8. 四种灯效时序
# ================================================================
def fig_effects():
    N = 8
    fig, axes = plt.subplots(4, 1, figsize=(7.8, 7.2))
    fig.subplots_adjust(left=0.095, right=0.985, top=0.905, bottom=0.06,
                        hspace=0.70)

    def draw(ax, masks, title, color):
        steps = len(masks)
        for s, m in enumerate(masks):
            for b in range(N):
                on = (m >> b) & 1
                ax.add_patch(Rectangle((s + 0.08, b + 0.08), 0.84, 0.84,
                                       fc=color if on else "#f4f4f4",
                                       ec="#bbbbbb", lw=0.5))
        ax.set_xlim(0, steps)
        ax.set_ylim(0, N)
        ax.set_yticks([b + 0.5 for b in range(N)])
        ax.set_yticklabels(["LED%d" % b for b in range(N)], fontsize=7.5)
        ax.set_xticks([s + 0.5 for s in range(steps)])
        ax.set_xticklabels([str(s) for s in range(steps)], fontsize=7.5)
        ax.set_xlabel("步数 step", fontsize=8)
        ax.set_title(title, fontsize=8.5, color=color, loc="left", pad=3)
        for sp in ax.spines.values():
            sp.set_color("#cccccc")

    masks1 = [1 << (s % N) for s in range(N)]
    draw(axes[0], masks1,
         "特效 1  单灯流水（间隔 200 ms）：始终只亮 1 个灯，亮点由 LED0 依次移到 LED7",
         C_RED)

    masks2 = [((1 << (s % N)) | (1 << ((s % N + N // 2) % N))) for s in range(N)]
    draw(axes[1], masks2,
         "特效 2  双灯追逐（间隔 200 ms）：两个亮点始终相隔 4 个位置同步右移",
         "#c96a1a")

    per = 2 * N - 2
    pos = [(s % per) if (s % per) < N else (per - (s % per)) for s in range(per)]
    masks3 = [1 << p for p in pos]
    draw(axes[2], masks3,
         "特效 3  乒乓往返（间隔 150 ms，周期 14 步）：亮点走到一端后折返，两端不重复",
         C_GRN)

    masks4 = [((1 << (s % (N + 1))) - 1) for s in range(N + 1)]
    draw(axes[3], masks4,
         "特效 4  逐个点亮再熄灭（间隔 120 ms）：点亮数由 0 逐级增到 8 后清零重来",
         C_PUR)

    fig.suptitle("四种跑马灯特效的灯态掩码时序（■ 表示该灯点亮）", fontsize=11.5,
                 y=0.982)
    save(fig, "fig08_effect_waveform.png")


# ================================================================
# 9. 呼吸灯 PWM 示意（选做）
# ================================================================
def fig_pwm():
    fig = plt.figure(figsize=(7.6, 5.0))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.15], hspace=0.62,
                          wspace=0.32, left=0.10, right=0.98, top=0.885,
                          bottom=0.10)

    ax = fig.add_subplot(gs[0, :])
    t = [i * 0.01 for i in range(200)]
    d = [50 * (1 - math.cos(2 * math.pi * (x / 2.0))) for x in t]
    ax.plot(t, d, color=C_PUR, lw=1.8)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 100)
    ax.set_xlabel("时间 / s", fontsize=8.5)
    ax.set_ylabel("占空比 / %", fontsize=8.5)
    ax.set_title("(a) 呼吸灯占空比控制曲线：2 s 完成一次“暗 → 亮 → 暗”",
                 fontsize=9.5, color=C_PUR, loc="left")
    ax.grid(ls=":", color="#cccccc")
    ax.tick_params(labelsize=8)
    ax.annotate("最暗\n占空比 ≈ 0", xy=(0, 0), xytext=(0.10, 30), fontsize=8,
                color="#666666", arrowprops=dict(arrowstyle="->", color="#999999"))
    ax.annotate("最亮\n占空比 ≈ 100%", xy=(1, 100), xytext=(1.38, 74), fontsize=8,
                color="#666666", ha="center",
                arrowprops=dict(arrowstyle="->", color="#999999"))

    titles = [("占空比 10%：平均电流小，灯偏暗", 0.10, C_RED),
              ("占空比 50%：平均电流中等，亮度适中", 0.50, C_ORG),
              ("占空比 90%：平均电流大，接近全亮", 0.90, C_GRN)]
    for k, (tt, duty, col) in enumerate(titles):
        ax = fig.add_subplot(gs[1, k])
        T, cycles = 1.0, 3
        xs, ys = [], []
        for c in range(cycles):
            xs += [c * T, c * T, c * T + duty * T, c * T + duty * T]
            ys += [0, 1, 1, 0]
        xs.append(cycles * T)
        ys.append(0)
        ax.plot(xs, ys, color=col, lw=1.6)
        ax.fill_between(xs, ys, color=col, alpha=0.18)
        ax.axhline(duty, color="#888888", ls="--", lw=0.9)
        ax.text(cycles * T * 0.5, duty + 0.10, "平均电压 = 占空比 × 3.3 V",
                fontsize=7.5, ha="center", color="#666666")
        ax.set_ylim(-0.12, 1.42)
        ax.set_xlim(0, cycles * T)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["0", "1"], fontsize=8)
        ax.set_xticks([])
        ax.set_xlabel("时间（PWM 周期 T）", fontsize=8)
        ax.set_title(tt, fontsize=8.5, color=col, loc="left")
        ax.grid(ls=":", color="#dddddd")
        ax.tick_params(labelsize=8)

    fig.suptitle("选做：PWM 占空比渐变实现呼吸灯的亮度调节原理", fontsize=11.5,
                 y=0.965)
    save(fig, "fig09_pwm_breath.png")


# ================================================================
# 10. 简化时钟树
# ================================================================
def fig_clock():
    fig, ax = canvas(7.2, 6.9, ylim=(0, 106))

    box(ax, 2, 74, 19, 14, "HSE 外部晶振\n25 MHz", fs=9.5, fc=C_GRN_F, ec=C_GRN)
    box(ax, 2, 56, 19, 12, "HSI 内部 RC\n16 MHz", fs=9.5, fc=C_GRAY_F, ec=C_GRAY)
    box(ax, 2, 38, 19, 12, "LSE 外部晶振\n32.768 kHz", fs=9, fc=C_GRAY_F,
        ec=C_GRAY)

    box(ax, 26, 56, 24, 30,
        "主 PLL\nPLLM = 25\nPLLN = 360\nPLLP = 2\nPLLQ = 4", fs=9.5,
        fc=C_BLUE_F, ec=C_BLUE)

    arrow(ax, (21, 81), (26, 79), color=C_GRN)
    tag(ax, 23.5, 84.5, "25 MHz", fs=8, color=C_GRN)
    arrow(ax, (21, 62), (26, 62), color=C_GRAY)
    tag(ax, 23.5, 65, "16 MHz", fs=8, color=C_GRAY)

    box(ax, 60, 66, 38, 17,
        "SYSCLK = 180 MHz\nAHB 预分频 ÷ 1\n（PLL 输出 360 MHz ÷ 2）", fs=9,
        fc=C_RED_F, ec=C_RED, bold=True)
    arrow(ax, (50, 74), (60, 74), color=C_BLUE)

    box(ax, 60, 48, 38, 12, "HCLK = 180 MHz\n（内核、AHB 总线、SysTick）", fs=8.5,
        fc=C_ORG_F, ec=C_ORG)
    arrow(ax, (79, 66), (79, 60), color=C_RED)

    box(ax, 60, 29, 38, 13, "APB1 预分频 ÷ 4\nPCLK1 = 45 MHz\n定时器时钟 90 MHz",
        fs=8.5, fc=C_ORG_F, ec=C_ORG)
    box(ax, 60, 12, 38, 13, "APB2 预分频 ÷ 2\nPCLK2 = 90 MHz\n定时器时钟 180 MHz",
        fs=8.5, fc=C_ORG_F, ec=C_ORG)

    arrow(ax, (79, 48), (79, 45), color=C_ORG)
    line(ax, [(69, 45), (89, 45)], color=C_ORG)
    arrow(ax, (69, 45), (69, 42), color=C_ORG)
    arrow(ax, (89, 45), (89, 25), color=C_ORG)

    box(ax, 2, 2, 96, 7,
        "Flash 等待周期 FLASH_LATENCY_5；电压调节 PWR_REGULATOR_VOLTAGE_SCALE1；"
        "APBx 定时器时钟自动 ×2", fs=8.5, fc=C_PUR_F, ec=C_PUR)

    tag(ax, 2, 99, "系统时钟树（HSE 25 MHz → SYSCLK 180 MHz）", fs=12, ha="left")

    save(fig, "fig10_clock_tree.png")


if __name__ == "__main__":
    fig_system()
    fig_pinmap()
    fig_schematic()
    fig_main_flow()
    fig_key_flow()
    fig_debounce()
    fig_modules()
    fig_effects()
    fig_pwm()
    fig_clock()
    print("done")
