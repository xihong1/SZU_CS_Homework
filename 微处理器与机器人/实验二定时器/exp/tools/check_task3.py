#!/usr/bin/env python
"""
验证任务三的三路 PWM。

默认只读寄存器 + 采样 CCR 波形。加上 --mode N 可以直接改写程序里的
模式变量, 不用真的按键就能切到任意模式验证 —— 写报告复现现象很方便。

模式编号:  0 = 同步呼吸   1 = 三色流水   2 = 警灯闪烁

用法:
    python tools/check_task3.py                    只看当前模式
    python tools/check_task3.py --mode 2           跳到警灯模式再看
    python tools/check_task3.py --mode 1 -d 5      跳到三色流水, 采样 5 秒
"""

import argparse
import subprocess
import sys
import time

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
ELF = "build/firmware.elf"

TIM3 = 0x40000400
CR1, CCER, PSC, ARR = 0x00, 0x20, 0x28, 0x2C
CCR2, CCR3, CCR4 = 0x38, 0x3C, 0x40

TIM_CLK = 90_000_000        # TIM3 挂 APB1, 45 MHz x 2

MODE_NAME = {0: "同步呼吸", 1: "三色流水", 2: "警灯闪烁"}


def sym(name):
    out = subprocess.run(["arm-none-eabi-nm", ELF],
                         capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        p = line.split()
        if len(p) == 3 and p[2] == name:
            return int(p[0], 16)
    return None


def bar(v, width=28, full=1000):
    n = int(v / full * width)
    return "#" * n + "." * (width - n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", type=int, choices=[0, 1, 2],
                    help="强制切换到指定模式 (0=同步呼吸 1=三色流水 2=警灯)")
    ap.add_argument("-d", "--duration", type=float, default=4.0,
                    help="采样秒数, 默认 4")
    args = ap.parse_args()

    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET, options={"frequency": 1_000_000}, blocking=False)
    if session is None:
        print("找不到探针")
        return 1

    with session:
        t = session.target
        t.halt()

        psc, arr = t.read32(TIM3 + PSC), t.read32(TIM3 + ARR)
        cr1, ccer = t.read32(TIM3 + CR1), t.read32(TIM3 + CCER)

        print("---- TIM3 配置 ----")
        print(f"  PSC = {psc}   ARR = {arr}   "
              f"PWM 频率 = {TIM_CLK / (psc + 1) / (arr + 1):.2f} Hz")
        print(f"  CR1 = 0x{cr1:08X}  CEN={(cr1 >> 0) & 1} ARPE={(cr1 >> 7) & 1}")
        print(f"  CCER= 0x{ccer:08X}  "
              f"CH2(红)={(ccer >> 4) & 1}  CH3(绿)={(ccer >> 8) & 1}  "
              f"CH4(蓝)={(ccer >> 12) & 1}")

        # ---- 可选: 强制切换模式 ----
        if args.mode is not None:
            addr = sym("s_mode")
            if addr is None:
                print("\n找不到 s_mode 符号, 无法强制切模式")
            else:
                t.write8(addr, args.mode)
                print(f"\n已把 s_mode 改写成 {args.mode} ({MODE_NAME[args.mode]})")

        # ---- 采样 ----
        print(f"\n---- CCR 采样 ({args.duration:.0f} s) ----")
        print("  CCR = 1000 - 亮度 (LED 低电平点亮), 所以 CCR 越小灯越亮")
        print()
        print(f"{'t(s)':>6} {'CCR2红':>8} {'CCR3绿':>8} {'CCR4蓝':>8}   "
              f"{'':>28}  亮度(红)")
        print("-" * 78)

        t.resume()
        t0 = time.time()
        while time.time() - t0 < args.duration:
            t.halt()
            c2 = t.read32(TIM3 + CCR2)
            c3 = t.read32(TIM3 + CCR3)
            c4 = t.read32(TIM3 + CCR4)
            t.resume()

            bright = (PWM_FULL := 1000) - c2
            print(f"{time.time() - t0:6.2f} {c2:8d} {c3:8d} {c4:8d}   "
                  f"{bar(bright)}")
            time.sleep(0.12)

        print()
        print("[判读]")
        print("  同步呼吸: 三路数值相同, 平滑地大范围来回变化")
        print("  三色流水: 三路数值出现明显相位差(一个在升, 另一个在降)")
        print("  警灯闪烁: 三路数值同时只在 0 和 1000 之间硬跳, 没有中间值")

    return 0


if __name__ == "__main__":
    sys.exit(main())
