/**
  ******************************************************************************
  * @file    tick.c
  * @brief   基本定时器 TIM6 —— 1 ms 系统时间基准
  ******************************************************************************
  */

#include "tick.h"
#include "main.h"

/* 1 ms 的毫秒计数 */
static volatile uint32_t s_tick_ms = 0;

volatile uint8_t g_tick_flag = 0;

static TIM_HandleTypeDef s_htim6;

/* ==========================================================================
 * 初始化
 * ========================================================================== */
void tick_init(void)
{
  __HAL_RCC_TIM6_CLK_ENABLE();

  /* ---- TIM6 时基 ----
   * TIM6 是基本定时器, 只有"向上计数 + 更新中断", 没有输入捕获/PWM 通道。
   * PSC = 89   -> 计数频率 90 MHz / 90 = 1 MHz
   * ARR = 999  -> 1 MHz / 1000 = 1 kHz, 即每 1 ms 产生一次更新事件
   */
  s_htim6.Instance               = TIM6;
  s_htim6.Init.Prescaler         = 89;
  s_htim6.Init.CounterMode       = TIM_COUNTERMODE_UP;
  s_htim6.Init.Period            = 999;
  s_htim6.Init.ClockDivision     = TIM_CLOCKDIVISION_DIV1;
  s_htim6.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  if (HAL_TIM_Base_Init(&s_htim6) != HAL_OK)
  {
    Error_Handler();
  }

  /* ---- 中断优先级 ----
   * 抢占优先级 2, 比 OLED 刷新的软件动作高, 保证 1 ms 节拍不丢。
   * 但中断体极短(仅计数+置标志), 不会影响主循环的实时性。
   */
  HAL_NVIC_SetPriority(TIM6_DAC_IRQn, 2, 0);
  HAL_NVIC_EnableIRQ(TIM6_DAC_IRQn);

  /* 开启更新中断并启动计数 */
  if (HAL_TIM_Base_Start_IT(&s_htim6) != HAL_OK)
  {
    Error_Handler();
  }
}

/* ==========================================================================
 * 时间读取
 * ========================================================================== */
uint32_t tick_now(void)
{
  return s_tick_ms;
}

/* ==========================================================================
 * 中断处理体
 *
 * 实验要求: 定时器中断里只允许计数和设置事件标志。
 * 所以这里只做两件事 —— 毫秒数 +1、置节拍标志, 然后立刻返回。
 * 千万不要在这里调用 HAL_Delay、disp_printf 或串口输出:
 *   1 ms 的中断里做这些耗时操作会严重挤占 CPU 时间, 甚至造成中断重入。
 * ========================================================================== */
void tick_isr(void)
{
  if (__HAL_TIM_GET_FLAG(&s_htim6, TIM_FLAG_UPDATE) == RESET)
  {
    return;
  }

  __HAL_TIM_CLEAR_FLAG(&s_htim6, TIM_FLAG_UPDATE);

  s_tick_ms++;
  g_tick_flag = 1;
}
