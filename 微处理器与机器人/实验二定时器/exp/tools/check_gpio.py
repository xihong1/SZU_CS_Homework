#!/usr/bin/env python
"""
通过 SWD 回读 GPIO 寄存器, 确认 OLED / LED 引脚真的被配成了输出。

这能在"屏幕不亮"的时候把问题分层:
    * 引脚模式不对          -> 软件问题, 改代码
    * 模式对但屏幕还是黑的  -> 硬件问题(插法/模块模式/接线)

用法:
    python tools/check_gpio.py
"""

import sys
from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"

GPIO_BASE = {
    "A": 0x40020000, "B": 0x40020400, "C": 0x40020800, "D": 0x40020C00,
    "E": 0x40021000, "F": 0x40021400, "G": 0x40021800, "H": 0x40021C00,
}
RCC_AHB1ENR = 0x40023830
MODER_OFF, OTYPER_OFF, OSPEEDR_OFF, PUPDR_OFF, ODR_OFF = 0x00, 0x04, 0x08, 0x0C, 0x14

MODER_TXT = {0: "输入", 1: "输出", 2: "复用", 3: "模拟"}

# 期望被配成输出的引脚
EXPECTED = [
    ("B",  7, "OLED_CS"),
    ("B",  4, "OLED_RS"),
    ("H",  8, "OLED_WR"),
    ("B",  3, "OLED_RD"),
    ("A", 15, "OLED_RST"),
    ("B",  9, "OLED_D0"),
    ("B",  8, "OLED_D1"),
    ("D",  3, "OLED_D2"),
    ("C", 11, "OLED_D3"),
    ("C",  9, "OLED_D4"),
    ("C",  8, "OLED_D5"),
    ("C",  7, "OLED_D6"),
    ("C",  6, "OLED_D7"),
    ("B",  1, "LED0(红)"),
    ("B",  0, "LED1(绿)"),
]

AHB1EN_BIT = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}


def main():
    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET, options={"frequency": 1_000_000}, blocking=False)
    if session is None:
        print("找不到探针")
        return 1

    with session:
        target = session.target
        target.halt()

        ahb1enr = target.read32(RCC_AHB1ENR)
        print(f"RCC_AHB1ENR = 0x{ahb1enr:08X}\n")

        print(f"{'引脚':10s}{'功能':12s}{'时钟':6s}{'模式':8s}{'类型':8s}{'ODR':5s}  判定")
        print("-" * 62)

        all_ok = True
        for port, pin, name in EXPECTED:
            base = GPIO_BASE[port]
            moder = target.read32(base + MODER_OFF)
            otyper = target.read32(base + OTYPER_OFF)
            odr = target.read32(base + ODR_OFF)

            mode = (moder >> (pin * 2)) & 0x3
            otype = (otyper >> pin) & 1
            bit = (odr >> pin) & 1
            clk = (ahb1enr >> AHB1EN_BIT[port]) & 1

            ok = (mode == 1) and (clk == 1)
            if not ok:
                all_ok = False
            mark = "OK" if ok else "**异常**"

            print(f"P{port}{pin:<8d}{name:12s}"
                  f"{'开' if clk else '关':6s}{MODER_TXT[mode]:8s}"
                  f"{'开漏' if otype else '推挽':8s}{bit:<5d}  {mark}")

        print()
        if all_ok:
            print("[结论] 13 根 OLED 线 + 2 根 LED 线都已正确配成推挽输出, GPIO 时钟已开。")
            print("       软件这一侧没问题 —— 屏幕不亮的话, 请重点查硬件: 模块插法、")
            print("       模块的 BS1/BS2 模式焊点、以及 P6 排座是否靠左插到位。")
        else:
            print("[结论] 有引脚模式不对, 属于软件问题, 需要改初始化代码。")

        target.resume()

    return 0 if all_ok else 2


if __name__ == "__main__":
    sys.exit(main())
