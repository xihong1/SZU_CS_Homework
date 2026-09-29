/**
  ******************************************************************************
  * @file    task4_freqmeter.c
  * @brief   任务四: 频率与占空比自测仪
  *
  * 接线:  PB1 (TIM3_CH4, PWM 输出)  ──跳线──  PA8 (TIM1_CH1, 捕获输入)
  ******************************************************************************
  */

#include "task4_freqmeter.h"
#include "app_debug.h"
#include "display.h"
#include "key.h"
#include "tick.h"
#include "gtim_pwm.h"
#include "gtim_ic.h"
#include <stdio.h>

/* 确认"断线"需要持续多久。
 * 单次读不到不一定是真断线(可能刚好赶上寄存器翻新), 持续这么久才算数。 */
#define NO_SIGNAL_MS    300U

/* 测量刷新间隔 */
#define MEAS_MS         200U

/* 测量值的合理范围。
 * 捕到的边沿不一定是我们要的信号(按键抖动、接线毛刺、悬空拾噪),
 * 那些情况算出来的频率往往离谱到不成样子。超出范围就按无效处理,
 * 屏幕上不会闪出无意义的乱码数值。 */
#define FREQ_MIN_HZ     10U
#define FREQ_MAX_HZ     200000U

/* 设定值 -> ARR 的换算。
 * PSC 固定 89, 所以 TIM3 的计数时钟是 1 MHz:  ARR = 1MHz / 目标频率 - 1 */
#define PSC_DIV         90U                      /* PSC = 89 -> 分频 90 */
#define PWM_CLK_HZ      (90000000UL / PSC_DIV)   /* = 1 MHz */

typedef struct
{
  const char *name;      /* 显示用名称 */
  uint32_t    freq_hz;   /* 设定频率 */
  uint32_t    duty_pct;  /* 设定占空比 (%) */
} test_point_t;

static const test_point_t s_points[] =
{
  { "100Hz",   100U, 25U },
  { "1kHz",   1000U, 50U },
  { "10kHz", 10000U, 75U },
};
#define POINT_NUM   (sizeof(s_points) / sizeof(s_points[0]))

/* 当前测试点。文件级 volatile, 方便用调试器直接改写做验证。 */
static volatile uint8_t s_point = 0;

/* ==========================================================================
 * 把相对误差格式化成 "+1.2%" 这样的字符串
 * @param permille : 误差, 单位千分之一 (即 5 表示 0.5%)
 * ========================================================================== */
static void fmt_err(char *buf, size_t n, int32_t permille)
{
  uint32_t a = (permille < 0) ? (uint32_t)(-permille) : (uint32_t)permille;
  (void)snprintf(buf, n, "%c%u.%u%%",
                 (permille < 0) ? '-' : '+',
                 (unsigned)(a / 10U), (unsigned)(a % 10U));
}

/* 相对误差, 单位千分之一: (meas - set) / set * 1000 */
static int32_t rel_permille(uint32_t meas, uint32_t set)
{
  if (set == 0U)
  {
    return 0;
  }
  return (int32_t)(((int32_t)meas - (int32_t)set) * 1000 / (int32_t)set);
}

/* ==========================================================================
 * 切换到第 idx 个测试点: 重设 ARR 和 CCR
 * ========================================================================== */
static void apply_point(uint8_t idx)
{
  uint32_t arr = (PWM_CLK_HZ / s_points[idx].freq_hz) - 1U;

  gtim_pwm_set_period((uint16_t)arr);

  /* CCR = (ARR+1) * 占空比
   * 这里用 gtim_pwm_set() 而不是 set_brightness():
   * 测量关心的是引脚上真实的占空比, 不需要按 LED 极性反相。 */
  uint16_t ccr = (uint16_t)(((uint32_t)arr + 1U) * s_points[idx].duty_pct / 100U);

  /* 三路都设成同样的占空比, 这样板上的 LED 亮度也跟着变, 现象更直观 */
  for (uint8_t ch = 0; ch < PWM_CH_NUM; ch++)
  {
    gtim_pwm_set(ch, ccr);
  }
}

/* ==========================================================================
 * 任务四主循环
 * ========================================================================== */
void task4_run(void)
{
  uint32_t last_meas = 0;
  uint32_t no_sig_ms = 0;         /* 开始读不到信号的时刻 */
  uint8_t  no_signal = 0;

  gtim_pwm_init();
  gtim_ic_init();
  apply_point(s_point);

  disp_clear();

  while (1)
  {
    if (!g_tick_flag)
    {
      continue;
    }
    g_tick_flag = 0;

    key_poll();

    /* KEY0 循环切换测试点 */
    if (key_take_press(KEY_0))
    {
      s_point = (uint8_t)((s_point + 1U) % POINT_NUM);
      apply_point(s_point);
      last_meas = 0;                 /* 立刻刷新显示 */
    }

    uint32_t now = tick_now();

    if ((uint32_t)(now - last_meas) < MEAS_MS)
    {
      continue;
    }
    last_meas = now;

    const test_point_t *tp = &s_points[s_point];

    /* ---- 读捕获结果 ----
     * "有信号"的判据就是: 能读到一组稳定数据, 而且数值落在合理范围内。
     * 读不到、或者频率/占空比离谱, 都说明当前输入的边沿不是我们要的信号。 */
    uint32_t period = 0, high = 0;
    uint8_t  ok = gtim_ic_read(&period, &high);

    uint32_t meas_freq = 0;
    uint32_t meas_duty = 0;

    if (ok)
    {
      /* 频率 = 捕获计数时钟 / 周期计数
       * 占空比 = 高电平计数 / 周期计数 */
      meas_freq = GTIM_IC_CLK_HZ / period;
      meas_duty = (uint32_t)((uint64_t)high * 100ULL / period);

      if (meas_freq < FREQ_MIN_HZ || meas_freq > FREQ_MAX_HZ || meas_duty > 100U)
      {
        ok = 0;                      /* 数值离谱 -> 不是有效信号 */
      }
    }

    /* ---- 断开判定 ----
     * 持续读不到才算真断线, 避免偶尔一次读失败就闪一下 "NO SIGNAL"。 */
    if (ok)
    {
      no_sig_ms = 0;
      no_signal = 0;
    }
    else if (no_sig_ms == 0U)
    {
      no_sig_ms = now;
    }
    else if ((uint32_t)(now - no_sig_ms) > NO_SIGNAL_MS)
    {
      no_signal = 1;
    }

    /* ---- 刷新显示 ---- */
    disp_printf(0, 0, "Task4 Freq Meter");
    disp_printf(1, 0, "SET %uHz %u%%", (unsigned)tp->freq_hz,
                (unsigned)tp->duty_pct);

    if (no_signal)
    {
      /* 明确显示"无信号", 测量值清空, 绝不保留上一次的旧数据 */
      disp_str_pad(2, 0, "GET  NO SIGNAL");
      disp_str_pad(3, 0, "ERR  --      ");
    }
    else if (!ok)
    {
      /* 还在确认中(刚拔线不久), 先显示中间状态, 不显示旧数据 */
      disp_str_pad(2, 0, "GET  ...     ");
      disp_str_pad(3, 0, "ERR  --      ");
    }
    else
    {
      char e_freq[12], e_duty[12];
      fmt_err(e_freq, sizeof(e_freq), rel_permille(meas_freq, tp->freq_hz));
      fmt_err(e_duty, sizeof(e_duty), rel_permille(meas_duty, tp->duty_pct));

      disp_printf(2, 0, "GET %uHz %u%%", (unsigned)meas_freq,
                  (unsigned)meas_duty);
      disp_printf(3, 0, "ERR %s %s", e_freq, e_duty);
    }

    g_dbg_loop_cnt++;
  }
}
