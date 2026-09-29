/**
  ******************************************************************************
  * @file    task2_reaction.c
  * @brief   任务二: 随机反应速度测试器
  ******************************************************************************
  */

#include "task2_reaction.h"
#include "app_config.h"
#include "display.h"
#include "led.h"
#include "key.h"
#include "tick.h"

/* ==========================================================================
 * 状态机
 * ========================================================================== */
typedef enum
{
  ST_IDLE = 0,     /* 等待开始 */
  ST_WAIT,         /* 随机等待 2~5 s, 此阶段按键算抢跑 */
  ST_CUE,          /* 提示 LED 已亮, 正在计时 */
  ST_RESULT,       /* 显示本次成绩 */
  ST_EARLY,        /* 抢跑 */
} rstate_t;

/* 随机等待范围: 2000 ~ 5000 ms */
#define WAIT_MIN_MS     2000U
#define WAIT_SPAN_MS    3001U

/* ==========================================================================
 * 伪随机数
 *
 * 用线性同余发生器(LCG)。种子里混入"按键那一刻的毫秒计数",
 * 而人的按键时刻是不确定的, 所以每次开局等到的时长都不一样。
 * 芯片没有真随机源, 这是没有 RTC/熵源时最实用的做法。
 * ========================================================================== */
static uint32_t s_rng = 0x12345678UL;

static uint32_t rng_next(void)
{
  s_rng = s_rng * 1103515245UL + 12345UL;
  return (s_rng >> 16) & 0x7FFFUL;
}

/* ==========================================================================
 * 显示刷新
 *
 * 只在"状态发生变化"时调用, 而不是每毫秒都刷。
 * 全屏重绘大约要 1 ms 量级, 如果放进 1 ms 的中断或者每毫秒都调,
 * 会挤占 CPU 并拖慢按键响应。
 * ========================================================================== */
static void draw(rstate_t st, uint32_t last_ms, uint32_t best_ms, uint8_t has_best)
{
  disp_str_pad(0, 0, "Task2: Reaction");

  switch (st)
  {
    case ST_IDLE:
      disp_str_pad(1, 0, "KEY0 to start");
      disp_str_pad(2, 0, "");
      break;

    case ST_WAIT:
      disp_str_pad(1, 0, "Wait for LED...");
      disp_str_pad(2, 0, "Don't rush!");
      break;

    case ST_CUE:
      disp_str_pad(1, 0, ">>> GO! <<<");
      disp_str_pad(2, 0, "Press KEY0!");
      break;

    case ST_RESULT:
      disp_printf(1, 0, "Time: %-4u ms", (unsigned)last_ms);
      disp_str_pad(2, 0, "");
      break;

    case ST_EARLY:
      disp_str_pad(1, 0, "FALSE START!");
      disp_str_pad(2, 0, "Pressed too soon");
      break;
  }

  if (has_best)
  {
    disp_printf(3, 0, "Best: %-4u ms", (unsigned)best_ms);
  }
  else
  {
    disp_str_pad(3, 0, "Best: -- ms");
  }
}

/* ==========================================================================
 * 任务二主循环
 * ========================================================================== */
void task2_run(void)
{
  rstate_t st       = ST_IDLE;
  uint32_t wait_ms  = 0;        /* 本次随机等待时长 */
  uint32_t t_ref    = 0;        /* 计时参考点 */
  uint32_t last_ms  = 0;        /* 本次成绩 */
  uint32_t best_ms  = 0;
  uint8_t  has_best = 0;

  led_off(LED_RED);

  disp_clear();

  /* 用上电以来的毫秒数做初始种子 */
  s_rng ^= tick_now();

  draw(st, last_ms, best_ms, has_best);

  while (1)
  {
    /* ---- 按 1 ms 节拍推进整个状态机 ----
     * 不在这里用 HAL_Delay 阻塞, 所以按键随时都能被响应。 */
    if (!g_tick_flag)
    {
      continue;
    }
    g_tick_flag = 0;

    key_poll();

    switch (st)
    {
      /* ---------------------------------------------------------------- */
      case ST_IDLE:
        /* KEY1: 清除最好成绩 */
        if (key_take_press(KEY_1))
        {
          has_best = 0;
          best_ms  = 0;
          draw(st, last_ms, best_ms, has_best);
        }
        /* KEY0: 开始一局 */
        if (key_take_press(KEY_0))
        {
          s_rng ^= tick_now();                          /* 混入人的按键时刻 */
          wait_ms = WAIT_MIN_MS + (rng_next() % WAIT_SPAN_MS);
          t_ref   = tick_now();
          led_off(LED_RED);
          st = ST_WAIT;
          draw(st, last_ms, best_ms, has_best);
        }
        break;

      /* ---------------------------------------------------------------- */
      case ST_WAIT:
        if (key_take_press(KEY_0))
        {
          /* 提示 LED 还没亮就按了 -> 抢跑 */
          st = ST_EARLY;
          draw(st, last_ms, best_ms, has_best);
        }
        else if ((uint32_t)(tick_now() - t_ref) >= wait_ms)
        {
          /* 时间到: 点亮提示 LED, 正式开始计时 */
          led_on(LED_RED);
          t_ref = tick_now();
          st = ST_CUE;
          draw(st, last_ms, best_ms, has_best);
        }
        break;

      /* ---------------------------------------------------------------- */
      case ST_CUE:
        if (key_take_press(KEY_0))
        {
          last_ms = tick_now() - t_ref;                 /* 反应时间 */
          led_off(LED_RED);

          if (!has_best || last_ms < best_ms)
          {
            best_ms  = last_ms;
            has_best = 1;
          }

          st = ST_RESULT;
          draw(st, last_ms, best_ms, has_best);
        }
        break;

      /* ---------------------------------------------------------------- */
      case ST_RESULT:
      case ST_EARLY:
        if (key_take_press(KEY_0))
        {
          st = ST_IDLE;
          draw(st, last_ms, best_ms, has_best);
        }
        break;

      default:
        st = ST_IDLE;
        break;
    }
  }
}
