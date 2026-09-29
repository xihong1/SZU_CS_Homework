/**
  ******************************************************************************
  * @file    task3_breath.c
  * @brief   任务三: 三色流水呼吸灯
  ******************************************************************************
  */

#include "task3_breath.h"
#include "app_debug.h"
#include "display.h"
#include "key.h"
#include "tick.h"
#include "gtim_pwm.h"

/* 每 15 ms 更新一次 CCR。
 * 太快没必要(1 kHz 的 PWM 周期才 1 ms, 但人眼看不出 60 Hz 以上的亮度变化),
 * 太慢则亮度台阶明显。15 ms 约 66 Hz, 已经足够平滑。 */
#define UPDATE_MS      15U

/* 相位表长度 = 正弦表长度, 一个完整周期覆盖 64 个相位点 */
#define PHASE_MAX      64U

/* 速度档位: 每次更新相位前进多少格 */
#define SPEED_MIN      1U
#define SPEED_MAX      8U

/* 刷新 OLED 上亮度读数的间隔 (ms) */
#define DISP_MS        300U

typedef enum
{
  MODE_SYNC = 0,     /* 同步呼吸 */
  MODE_FLOW,         /* 三色流水 */
  MODE_STROBE,       /* 警灯闪烁 */
  MODE_COUNT
} bmode_t;

static const char *const s_mode_name[MODE_COUNT] =
{
  "Sync breath",
  "Color flow",
  "Strobe",
};

/* 当前模式。
 * 特意声明成文件级 volatile, 好处是可以用调试器(SWD)直接改写这个变量,
 * 不用真的按键就能切到任意模式做验证 —— 写报告时复现现象很方便。
 * 配合 tools/check_task3.py 使用。 */
static volatile uint8_t s_mode = MODE_SYNC;

/* 64 点正弦表, 取值 0~1000, 覆盖一个完整呼吸周期。
 * 用正弦而不是三角波, 是因为三角函数在最高点和最低点变化平缓,
 * 呼吸的"停顿感"更自然, 不会出现明显的折点。 */
static const uint16_t s_sine[64] =
{
     0,    2,   10,   22,   38,   59,   84,  113,
   146,  183,  222,  264,  309,  355,  402,  451,
   500,  549,  598,  645,  691,  736,  778,  817,
   854,  887,  916,  941,  962,  978,  990,  998,
  1000,  998,  990,  978,  962,  941,  916,  887,
   854,  817,  778,  736,  691,  645,  598,  549,
   500,  451,  402,  355,  309,  264,  222,  183,
   146,  113,   84,   59,   38,   22,   10,    2,
};

/* ==========================================================================
 * 根据模式和相位算出三路亮度
 *
 * 亮度范围 0~PWM_PERIOD, 由 gtim_pwm_set_brightness() 负责换成 CCR。
 * ========================================================================== */
static void calc_rgb(bmode_t mode, uint32_t phase, uint32_t speed, uint32_t now,
                     uint16_t *r, uint16_t *g, uint16_t *b)
{
  switch (mode)
  {
    /* 三路同相位: 红绿蓝一起变亮变暗, 合成白光呼吸 */
    case MODE_SYNC:
      *r = s_sine[phase];
      *g = s_sine[phase];
      *b = s_sine[phase];
      break;

    /* 三路相位各差 1/3 个周期 (64/3 = 21.3 格), 颜色依次交接 */
    case MODE_FLOW:
      *r = s_sine[phase];
      *g = s_sine[(phase + 21U) % PHASE_MAX];
      *b = s_sine[(phase + 43U) % PHASE_MAX];
      break;

    /* 警灯闪烁: 三色一起快速全亮 / 全灭, 硬切换而不是渐变。
     * 用挂钟时间(而不是相位)决定开关, 这样闪烁频率和速度档位一一对应,
     * 不会因为相位步进变大而快到看不出"闪"。 */
    case MODE_STROBE:
    {
      /* 各速度档位对应的半周期 (ms): 1 档最慢, 8 档最快 */
      static const uint16_t half_ms[SPEED_MAX] =
      {
        300, 240, 190, 150, 120, 95, 75, 60
      };
      uint8_t on = (uint8_t)(((now / half_ms[speed - 1U]) & 1U) == 0U);

      *r = on ? PWM_PERIOD : 0U;
      *g = on ? PWM_PERIOD : 0U;
      *b = on ? PWM_PERIOD : 0U;
      break;
    }

    default:
      *r = *g = *b = 0U;
      break;
  }
}

/* ==========================================================================
 * 任务三主循环
 * ========================================================================== */
void task3_run(void)
{
  uint32_t phase      = 0;
  uint32_t speed      = SPEED_MIN;
  uint32_t last_upd   = 0;
  uint32_t last_disp  = 0;
  uint8_t  need_disp  = 1;
  uint16_t r = 0, g = 0, b = 0;

  gtim_pwm_init();
  disp_clear();

  while (1)
  {
    if (!g_tick_flag)
    {
      continue;
    }
    g_tick_flag = 0;

    key_poll();

    /* ---- 按键: KEY0 换模式, KEY1 加快, KEY2 减慢 ---- */
    if (key_take_press(KEY_0))
    {
      s_mode = (uint8_t)((s_mode + 1U) % MODE_COUNT);
      phase = 0;
      need_disp = 1;
    }
    if (key_take_press(KEY_1) && speed < SPEED_MAX)
    {
      speed++;
      need_disp = 1;
    }
    if (key_take_press(KEY_2) && speed > SPEED_MIN)
    {
      speed--;
      need_disp = 1;
    }

    uint32_t now = tick_now();

    /* ---- 按固定节拍推进相位, 平滑改变占空比 ---- */
    if ((uint32_t)(now - last_upd) >= UPDATE_MS)
    {
      last_upd = now;

      phase = (phase + speed) % PHASE_MAX;
      calc_rgb((bmode_t)s_mode, phase, speed, now, &r, &g, &b);

      gtim_pwm_set_brightness(PWM_CH_R, r);
      gtim_pwm_set_brightness(PWM_CH_G, g);
      gtim_pwm_set_brightness(PWM_CH_B, b);

      g_dbg_loop_cnt++;
    }

    /* ---- 刷新显示 ----
     * 只在需要时刷(换模式/调速度), 另外每 300 ms 更新一次实时亮度读数。
     * 不做每毫秒全屏重绘: 全屏重绘要 1 ms 量级, 会把按键响应拖慢。 */
    if (need_disp || (uint32_t)(now - last_disp) >= DISP_MS)
    {
      need_disp = 0;
      last_disp = now;

      disp_str_pad(0, 0, "Task3: RGB PWM");
      disp_printf(1, 0, "Mode: %s", s_mode_name[s_mode]);
      disp_printf(2, 0, "Speed: %u  (K1/K2)", (unsigned)speed);

      /* 显示实时亮度百分比, 可以直观看到三路占空比在变化 */
      disp_printf(3, 0, "R%3u G%3u B%3u",
                  (unsigned)(r * 100U / PWM_PERIOD),
                  (unsigned)(g * 100U / PWM_PERIOD),
                  (unsigned)(b * 100U / PWM_PERIOD));
    }
  }
}
