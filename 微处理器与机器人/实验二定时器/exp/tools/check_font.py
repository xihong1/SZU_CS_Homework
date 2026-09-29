#!/usr/bin/env python
"""
从芯片 FLASH 里把字库读回来解码成点阵, 确认真正烧进去的字节是对的。

为什么要读芯片而不是读本地的 oledfont.h:
    本地头文件是对的, 不代表二进制里是对的 —— 中间还隔着
    "改头文件有没有触发 .c 重编" 这一关。直接从目标芯片回读,
    才能证明屏幕上显示的就是我们想要的数据。

用法:
    python tools/check_font.py [字符...]      默认检查 A 8 g p
"""

import subprocess
import sys

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
ELF = "build/firmware.elf"
CHARS = sys.argv[1:] or ["A", "8", "g", "p"]


def symbol_addr(name):
    out = subprocess.run(["arm-none-eabi-nm", ELF],
                         capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] == name:
            return int(parts[0], 16)
    raise SystemExit(f"找不到符号 {name}")


def main():
    base = symbol_addr("oled_asc2_1608")
    print(f"字库符号 oled_asc2_1608 @ 0x{base:08X}\n")

    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET, options={"frequency": 1_000_000}, blocking=False)
    if session is None:
        print("找不到探针")
        return 1

    with session:
        target = session.target
        target.halt()

        for ch in CHARS:
            idx = ord(ch) - 32
            data = target.read_memory_block8(base + idx * 16, 16)

            print(f"--- '{ch}'  (索引 {idx}, 地址 0x{base + idx*16:08X}) ---")
            print("    " + " ".join(f"{b:02X}" for b in data))
            for page in range(2):
                for bit in range(8):
                    line = ""
                    for col in range(8):
                        line += "#" if (data[page * 8 + col] >> bit) & 1 else "."
                    print("    " + line)
            print()

        target.resume()

    print("[说明] 上面的图案如果字形正确(比如 A 像 A), 说明烧进芯片的字库位序是对的。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
