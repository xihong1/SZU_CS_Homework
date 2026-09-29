#!/usr/bin/env python
"""
验证任务四: 频率与占空比自测仪。

从 TIM5 的捕获寄存器读出周期/高电平计数, 自己算一遍频率、占空比和相对误差,
再和 TIM3 的设定值对比 —— 也就是把 OLED 上"应该显示的数字"在电脑上验算一遍。

用法:
    python tools/check_task4.py                 读当前测试点
    python tools/check_task4.py --point 1       先切到第 2 个测试点(1kHz/50%)再读
    python tools/check_task4.py -n 5            连续采 5 组看稳定性
"""

import argparse
import subprocess
import sys
import time

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
ELF = "build/firmware.elf"

TIM3 = 0x40000400       # PWM 输出
TIM5 = 0x40000C00       # 输入捕获

T5_CR1, T5_PSC, T5_ARR, T5_CCR1, T5_CCR2 = 0x00, 0x28, 0x2C, 0x34, 0x38
T3_PSC, T3_ARR, T3_CCR4 = 0x28, 0x2C, 0x40

IC_CLK = 10_000_000     # TIM5 计数时钟 10 MHz (PSC=8)
TIM_CLK = 90_000_000    # APB1 定时器时钟 90 MHz (PSC=89 -> 1 MHz 计数)

POINTS = [
    ("100 Hz / 25%",   100,  25),
    ("1 kHz / 50%",   1000,  50),
    ("10 kHz / 75%", 10000,  75),
]


def sym(name):
    out = subprocess.run(["arm-none-eabi-nm", ELF],
                         capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        p = line.split()
        if len(p) == 3 and p[2] == name:
            return int(p[0], 16)
    return None


def err_permille(meas, setting):
    """相对误差, 单位千分之一 (千分比)"""
    if setting == 0:
        return 0
    return round((meas - setting) * 1000 / setting)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--point", type=int, choices=[0, 1, 2], help="先切到指定测试点")
    ap.add_argument("-n", "--count", type=int, default=1, help="采样组数")
    args = ap.parse_args()

    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET, options={"frequency": 1_000_000}, blocking=False)
    if session is None:
        print("找不到探针")
        return 1

    with session:
        t = session.target
        t.halt()

        if args.point is not None:
            addr = sym("s_point")
            if addr is not None:
                t.write8(addr, args.point)
                print(f"已切到测试点 {args.point + 1}: {POINTS[args.point][0]}\n")
                t.resume(); time.sleep(0.5); t.halt()

        # ---- TIM3 实际输出的是什么 ----
        psc = t.read32(TIM3 + T3_PSC)
        arr = t.read32(TIM3 + T3_ARR)
        ccr = t.read32(TIM3 + T3_CCR4)
        # 频率 = 90MHz / (PSC+1) / (ARR+1)
        set_freq = TIM_CLK / (psc + 1) / (arr + 1)
        set_duty = ccr * 100.0 / (arr + 1)

        print("---- TIM3 (PWM 输出, 实际产生的信号) ----")
        print(f"  PSC={psc} ARR={arr} CCR4={ccr}")
        print(f"  实际设定: {set_freq:.2f} Hz   {set_duty:.2f} %")

        # ---- TIM5 捕获到了什么 ----
        print(f"\n---- TIM5 (输入捕获) ----")
        print(f"{'#':>3} {'周期计数':>10} {'高电平计数':>12} "
              f"{'实测频率':>12} {'实测占空比':>12}   {'误差(频率/占空比)':>20}")
        print("-" * 82)

        t.resume()
        for i in range(args.count):
            time.sleep(0.25)
            t.halt()
            p1 = t.read32(TIM5 + T5_CCR1)
            h = t.read32(TIM5 + T5_CCR2)
            t.resume()

            if p1 == 0:
                print(f"{i+1:>3} {'未捕获到信号 (NO SIGNAL)':>40}")
                continue

            meas_f = IC_CLK / p1
            meas_d = h * 100.0 / p1
            ef = err_permille(meas_f, set_freq)
            ed = err_permille(meas_d, set_duty)

            print(f"{i+1:>3} {p1:>10} {h:>12} "
                  f"{meas_f:>10.2f}Hz {meas_d:>11.2f}%   "
                  f"{ef/10:>+8.2f}% {ed/10:>+8.2f}%")

        print()
        print("[说明] 一列误差 = 实测值相对设定值的偏差, 单位是百分比。")
        print("       两个误差都应该在 ±0.2% 以内 —— 因为 PWM 和捕获用的是")
        print("       同一个 90 MHz 定时器时钟, 唯一的误差来源是 ±1 个计数的量化误差。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
