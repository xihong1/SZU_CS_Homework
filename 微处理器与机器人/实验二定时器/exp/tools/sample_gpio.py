#!/usr/bin/env python
"""
持续采样 GPIOA / GPIOB 的输出电平, 用来确认固件到底有没有在驱动引脚。

配合 LED 自检固件使用: 采样结果里应该能看到 PB0 / PB1 / PA7 / PA8
依次被拉低 3 秒再拉高 3 秒, 最后四个一起拉低。

如果 ODR 显示引脚确实在翻转, 但肉眼看灯不亮, 那问题就 100% 在硬件侧
(虚焊、插错排针、灯坏了、杜邦线没插到底)。

用法:
    python tools/sample_gpio.py [采样秒数]      默认 32 秒
"""

import sys
import time

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
GPIOA_ODR = 0x40020014
GPIOB_ODR = 0x40020414

WATCH = [("A", 7, "PA7"), ("A", 8, "PA8"), ("B", 0, "PB0"), ("B", 1, "PB1")]

DURATION = float(sys.argv[1]) if len(sys.argv) > 1 else 32.0
INTERVAL = 0.4


def main():
    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET, options={"frequency": 1_000_000}, blocking=False)
    if session is None:
        print("找不到探针")
        return 1

    with session:
        target = session.target

        header = "  t(s)  " + "".join(f"{n:>7s}" for _, _, n in WATCH)
        print(header)
        print("-" * len(header))

        t0 = time.time()
        last = None
        while time.time() - t0 < DURATION:
            # 采一次就读一次, 不长时间停机, 尽量少干扰程序运行
            target.halt()
            a = target.read32(GPIOA_ODR)
            b = target.read32(GPIOB_ODR)
            target.resume()

            vals = []
            for port, pin, _ in WATCH:
                reg = a if port == "A" else b
                vals.append("HIGH" if (reg >> pin) & 1 else "LOW")

            row = (round(time.time() - t0, 1), tuple(vals))
            if row[1] != last:            # 只在状态变化时打印, 表格更清爽
                print(f"{row[0]:6.1f}  " + "".join(f"{v:>7s}" for v in vals))
                last = row[1]

            time.sleep(INTERVAL)

        print()
        print("[说明] 只要这里看到 PA7/PA8/PB0/PB1 在 LOW/HIGH 之间变化,")
        print("       就说明固件在正确驱动它们; 灯不亮就是接线侧的问题。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
