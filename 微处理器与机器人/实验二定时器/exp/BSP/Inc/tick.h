/**
  ******************************************************************************
  * @file    tick.h
  * @brief   基本定时器 TIM6 提供的 1 ms 系统时间基准
  *
  * 时钟计算 (TIM6 挂 APB1):
  *     APB1 总线 = 180 MHz / 4 = 45 MHz
  *     APB1 预分频系数 >= 2, 所以定时器时钟 = 2 x 45 MHz = 90 MHz
  *
  *     要 1 ms 更新一次:
  *         90 MHz / ((PSC+1)(ARR+1)) = 1000 Hz
  *         (PSC+1)(ARR+1) = 90000
  *     取 PSC = 89  ->  计数时钟 = 90 MHz / 90 = 1 MHz (分辨率 1 us)
  *        ARR = 999 ->  每 1000 个计数溢出一次 = 1 ms
  *
  * 中断服务程序里只做"计数 + 置标志"两件事, 不做任何显示或串口输出 ——
  * 这是实验要求明确规定的。
  ******************************************************************************
  */

#ifndef __TICK_H
#define __TICK_H

#include "stm32f4xx_hal.h"

/* 每秒 tick 数 / 每毫秒 tick 数 */
#define TICK_HZ         1000U
#define TICK_PER_MS     1U

void tick_init(void);

/* 当前毫秒计数 (单调递增, 约 49.7 天溢出一次) */
uint32_t tick_now(void);

/* 定时器中断入口, 由 stm32f4xx_it.c 的 TIM6_DAC_IRQHandler 调用 */
void tick_isr(void);

/* 主循环用的节拍标志: 每次 1 ms 中断置 1, 主循环取走后清零。
 * 这样主循环可以按"每毫秒处理一次"的节奏跑, 又不必在中断里做重活。 */
extern volatile uint8_t g_tick_flag;

#endif /* __TICK_H */
