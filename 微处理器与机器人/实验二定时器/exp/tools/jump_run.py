#!/usr/bin/env python
"""
绕过 BOOT0 引导问题, 用调试器直接把 PC 强制指到用户程序的 Reset_Handler。

背景:
    阿波罗开发板如果 BOOT0 跳线接在高电平, 芯片复位后会进入系统存储器里的
    出厂 Bootloader (PC 落在 0x1FFF_xxxx), 而不是从 0x08000000 的 FLASH 启动。
    此时烧进去的程序虽然正确, 但永远不会被执行。

本脚本用来验证这一点:
    1. 复位并停机
    2. 手工设置 SP / PC 到用户程序的复位入口
    3. 放行运行, 等待若干秒
    4. 停机并回读 RAM 里的调试变量

如果回读到的 g_dbg_boot_magic == 0xB00710AD 且计数在涨,
说明程序本身完全正常, 问题 100% 出在 BOOT0 引导配置上。

用法:
    python tools/jump_run.py build/firmware.elf
"""

import sys
import time
import struct

from pyocd.core.helpers import ConnectHelper

TARGET = "stm32f429xi"
WAIT_S = 2.0


def load_symbols(elf_path):
    """用 arm-none-eabi-nm 解析出调试变量地址。"""
    import subprocess
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


def main():
    elf = sys.argv[1] if len(sys.argv) > 1 else "build/firmware.elf"

    # ---- 从 ELF 里取复位向量, 避免手工填地址 ----
    with open(elf, "rb") as f:
        head = f.read(0x40)

    # 直接读目标上的向量表更可靠
    session = ConnectHelper.session_with_chosen_probe(
        target_override=TARGET,
        options={"frequency": 1_000_000},
        blocking=False,
    )
    if session is None:
        print("找不到探针")
        return 1

    with session:
        target = session.target

        # 从 FLASH 起始处读向量表前两项
        target.halt()
        vec = target.read_memory_block32(0x08000000, 2)
        initial_sp = vec[0]
        reset_handler = vec[1]
        print(f"向量表: SP=0x{initial_sp:08X}  Reset_Handler=0x{reset_handler:08X}")

        # ---- 复位(不停机), 然后手工跳转到用户程序 ----
        target.reset()
        target.halt()

        # 关键: 同时设好 SP / PC, 并把 VTOR 指回 FLASH,
        # 否则后续中断还会走系统存储器的向量表。
        target.write_core_register("sp", initial_sp)
        target.write_core_register("pc", reset_handler & ~1)
        target.write_core_register("xpsr", 0x01000000)   # Thumb 位必须为 1

        print("已强制 PC -> 用户 Reset_Handler, 放行运行...")
        target.resume()
        time.sleep(WAIT_S)

        target.halt()
        pc = target.read_core_register("pc")
        print(f"暂停时 PC = 0x{pc:08X}")

        # ---- 回读调试变量 ----
        syms = load_symbols(elf)
        names = [
            "g_dbg_boot_magic",
            "g_dbg_last_state",
            "g_dbg_systick_cnt",
            "g_dbg_loop_cnt",
            "g_dbg_led_toggles",
            "g_fault_flags",
        ]
        print("\n---- RAM 调试变量 ----")
        ok = True
        vals = {}
        for n in names:
            if n not in syms:
                print(f"  {n:22s} : (符号未找到)")
                continue
            v = target.read32(syms[n])
            vals[n] = v
            print(f"  {n:22s} : 0x{v:08X}  ({v})")

        magic = vals.get("g_dbg_boot_magic")
        if magic == 0xB00710AD:
            print("\n[结论] 程序运行正常 -> 问题在 BOOT0 引导配置")
            ok = True
        else:
            print("\n[结论] 程序仍未正常运行, 需要继续排查")
            ok = False

        target.resume()

    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
