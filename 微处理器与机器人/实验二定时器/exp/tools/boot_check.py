#!/usr/bin/env python
"""
判断芯片复位后到底从哪里启动 (单次会话内完成, 排除"重连是否复位"的干扰)。

流程:
    connect -> reset -> resume -> 等待 -> halt -> 读 PC / 读调试变量

判据:
    * g_dbg_boot_magic == 0xB00710AD 且 PC 落在 0x0800_xxxx
        => 从内部 FLASH 正常启动, 程序在跑。
    * PC 落在 0x1FFF_xxxx, RAM 里没有 magic
        => 芯片停在系统存储器(出厂 Bootloader)里, 说明 BOOT0 被拉高了。

用法:
    python tools/boot_check.py
"""

import subprocess
import sys
import time

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
ELF = "build/firmware.elf"
MAGIC = 0xB00710AD
WAIT_S = 2.0


def load_symbols(elf_path):
    out = subprocess.run(
        ["arm-none-eabi-nm", "-n", elf_path],
        capture_output=True, text=True, check=True
    ).stdout
    syms = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3:
            syms[parts[2]] = int(parts[0], 16)
    return syms


def region(pc):
    if 0x08000000 <= pc < 0x08100000:
        return "内部 FLASH  (用户程序)"
    if 0x1FFF0000 <= pc < 0x20000000:
        return "系统存储器  (出厂 Bootloader / ISP)"
    if 0x20000000 <= pc < 0x20030000:
        return "内部 SRAM"
    return "未知区域"


def main():
    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET,
        options={"frequency": 1_000_000},
        blocking=False,
    )
    if session is None:
        print("找不到探针")
        return 1

    syms = load_symbols(ELF)

    with session:
        target = session.target

        # ---- 纯复位, 不人为干预 PC ----
        target.reset()
        target.resume()
        time.sleep(WAIT_S)
        target.halt()

        def rd(name):
            """符号可能被 --gc-sections 回收(某段代码不可达时), 缺失就返回 None。"""
            a = syms.get(name)
            return target.read32(a) if a is not None else None

        pc    = target.read_core_register("pc")
        magic = rd("g_dbg_boot_magic")
        state = rd("g_dbg_last_state")
        syst  = rd("g_dbg_systick_cnt")
        togg  = rd("g_dbg_led_toggles")
        loops = rd("g_dbg_loop_cnt")

        print(f"复位后运行 {WAIT_S:.0f} s, 停机:")
        print(f"  PC                    = 0x{pc:08X}   [{region(pc)}]")
        print(f"  g_dbg_boot_magic      = {f'0x{magic:08X}' if magic is not None else '(已回收)'}")
        print(f"  g_dbg_last_state      = {f'0x{state:08X}' if state is not None else '(已回收)'}")
        print(f"  g_dbg_systick_cnt     = {syst}")
        print(f"  g_dbg_loop_cnt        = {loops}")
        print(f"  g_dbg_led_toggles     = {togg}")
        print()

        if magic == MAGIC and 0x08000000 <= pc < 0x08100000:
            print("[结论] 芯片从内部 FLASH 正常启动, 用户程序正在运行。")
            rc = 0
        else:
            print("[结论] 芯片没有运行用户程序 —— 停在系统存储器 Bootloader 里。")
            print("       原因: BOOT0 被拉高。请把开发板 BOOT0 跳线/拨码接到 GND(0),")
            print("       然后复位, 程序就会从 FLASH 正常启动。")
            rc = 2

        target.resume()

    return rc


if __name__ == "__main__":
    sys.exit(main())
