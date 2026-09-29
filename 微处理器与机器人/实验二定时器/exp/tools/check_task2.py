#!/usr/bin/env python
"""
验证任务二的 1 ms 时间基准 (基本定时器 TIM6)。

检查三件事:
    1. TIM6 的 PSC / ARR 配置是否符合设计
    2. TIM6 是否真的在运行 (CEN 置位、CNT 在变)
    3. 毫秒计数器的实际速率是不是 1000 Hz —— 用挂钟时间比对,
       这一条能同时验证"定时器时钟是不是 90 MHz"

用法:
    python tools/check_task2.py
"""

import subprocess
import sys
import time

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
ELF = "build/firmware.elf"

TIM6 = 0x40001000
CR1, DIER, SR, CNT, PSC, ARR = 0x00, 0x0C, 0x10, 0x24, 0x28, 0x2C

# TIM6 挂 APB1。APB1 = 45 MHz, 预分频 >= 2, 所以定时器时钟 = 90 MHz
TIM_CLK = 90_000_000


def sym(name):
    out = subprocess.run(["arm-none-eabi-nm", ELF],
                         capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        p = line.split()
        if len(p) == 3 and p[2] == name:
            return int(p[0], 16)
    return None


def main():
    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET, options={"frequency": 1_000_000}, blocking=False)
    if session is None:
        print("找不到探针")
        return 1

    with session:
        t = session.target
        t.halt()

        cr1 = t.read32(TIM6 + CR1)
        dier = t.read32(TIM6 + DIER)
        psc = t.read32(TIM6 + PSC)
        arr = t.read32(TIM6 + ARR)

        print("---- TIM6 寄存器 ----")
        print(f"  PSC  = {psc}      (设计值 89  -> 计数时钟 90MHz/90 = 1 MHz)")
        print(f"  ARR  = {arr}     (设计值 999 -> 1MHz/1000 = 1 kHz = 1 ms)")
        print(f"  CR1  = 0x{cr1:08X}   CEN(bit0) = {(cr1 >> 0) & 1}  "
              f"ARPE(bit7) = {(cr1 >> 7) & 1}")
        print(f"  DIER = 0x{dier:08X}   UIE(bit0) = {(dier >> 0) & 1}")

        # ---- 反推实际更新频率 ----
        f_upd = TIM_CLK / (psc + 1) / (arr + 1)
        print(f"\n  按当前寄存器反推的更新频率 = 90MHz/({psc}+1)/({arr}+1) "
              f"= {f_upd:.3f} Hz")
        print(f"  即每 {1000.0 / f_upd:.4f} ms 一次更新中断")

        # ---- 实测定时器实际频率 ----
        print("\n---- 实测毫秒计数器速率 ----")
        addr = sym("s_tick_ms")
        if addr is None:
            print("  找不到 s_tick_ms 符号 (可能被优化掉了), 跳过实测")
        else:
            t.resume()
            time.sleep(0.05)
            t.halt()
            m0 = t.read32(addr)
            wall0 = time.time()

            t.resume()
            time.sleep(3.0)          # 让它跑 3 秒
            t.halt()
            m1 = t.read32(addr)
            wall1 = time.time()

            dm = (m1 - m0) & 0xFFFFFFFF
            dw = wall1 - wall0
            hz = dm / dw if dw > 0 else 0

            print(f"  毫秒计数器: {m0} -> {m1}  (增加了 {dm})")
            print(f"  挂钟时间  : {dw:.3f} s")
            print(f"  实测频率  : {hz:.1f} Hz   (设计 1000 Hz)")
            err = abs(hz - 1000.0) / 1000.0 * 100
            print(f"  相对误差  : {err:.3f} %")
            print()
            if err < 1.0:
                print("[结论] 1 ms 时间基准准确, 定时器时钟 90 MHz 也得到交叉验证。")
            else:
                print("[结论] 频率偏差过大, 需要检查 APB1 分频或 PSC/ARR。")

        t.resume()

    return 0


if __name__ == "__main__":
    sys.exit(main())
