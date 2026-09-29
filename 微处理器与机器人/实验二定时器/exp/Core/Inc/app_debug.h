/**
  ******************************************************************************
  * @file    app_debug.h
  * @brief   调试观察变量
  *
  * 这些变量放在 RAM 里, 可以用 pyOCD 通过 SWD 直接回读, 不依赖肉眼观察
  * 屏幕或 LED。板子跑飞、屏幕不亮、现象对不上时, 先把它们读出来,
  * 就能立刻知道程序执行到了哪一步、中断有没有在跑。
  *
  * 回读方法:  python tools/boot_check.py
  ******************************************************************************
  */

#ifndef __APP_DEBUG_H
#define __APP_DEBUG_H

#include <stdint.h>

extern volatile uint32_t g_dbg_boot_magic;    /* 期望 0xB00710AD, 证明程序真的跑起来了 */
extern volatile uint32_t g_dbg_last_state;    /* 执行阶段标记, 见 main.c 的 STAGE_xxx */
extern volatile uint32_t g_dbg_systick_cnt;   /* SysTick 中断次数 (HAL 的 1 ms 时基) */
extern volatile uint32_t g_dbg_loop_cnt;      /* 主循环计数 */
extern volatile uint32_t g_dbg_led_toggles;   /* LED 翻转次数 */
extern volatile uint32_t g_fault_flags;       /* 硬件错误标志, 0 = 正常 */

#define DBG_BOOT_MAGIC   0xB00710ADUL

#endif /* __APP_DEBUG_H */
