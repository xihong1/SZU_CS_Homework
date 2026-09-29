/**
  ******************************************************************************
  * @file    debug_led.c
  * @brief   LED 接线自检
  ******************************************************************************
  */

#include "debug_led.h"
#include "app_debug.h"
#include "display.h"

/* 每个电平保持多久 (ms) */
#define PHASE_MS   3000U

typedef struct
{
  GPIO_TypeDef *port;
  uint16_t      pin;
  const char   *name;
} test_pin_t;

static const test_pin_t s_pins[4] =
{
  { GPIOB, GPIO_PIN_0, "PB0" },
  { GPIOB, GPIO_PIN_1, "PB1" },
  { GPIOA, GPIO_PIN_7, "PA7" },
  { GPIOA, GPIO_PIN_8, "PA8" },
};

static void drive_all(uint8_t low)
{
  for (int i = 0; i < 4; i++)
  {
    /* BSRR: 低 16 位置 1 -> 输出高; 高 16 位置 1 -> 输出低 */
    s_pins[i].port->BSRR = low ? ((uint32_t)s_pins[i].pin << 16)
                               : ((uint32_t)s_pins[i].pin);
  }
}

void debug_led_run(void)
{
  GPIO_InitTypeDef gpio = {0};

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  gpio.Mode  = GPIO_MODE_OUTPUT_PP;
  gpio.Pull  = GPIO_NOPULL;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;
  for (int i = 0; i < 4; i++)
  {
    gpio.Pin = s_pins[i].pin;
    HAL_GPIO_Init(s_pins[i].port, &gpio);
  }

  while (1)
  {
    /* ---- 第一阶段: 逐个引脚, 拉低 3 s / 拉高 3 s ---- */
    for (int i = 0; i < 4; i++)
    {
      disp_clear();
      disp_printf(0, 0, "LED TEST  %d/4", i + 1);
      disp_printf(1, 0, "Pin  : %s", s_pins[i].name);
      disp_printf(2, 0, "Level: LOW");

      s_pins[i].port->BSRR = (uint32_t)s_pins[i].pin << 16;
      HAL_Delay(PHASE_MS);

      disp_printf(2, 0, "Level: HIGH");
      s_pins[i].port->BSRR = s_pins[i].pin;
      HAL_Delay(PHASE_MS);

      g_dbg_loop_cnt++;
    }

    /* ---- 第二阶段: 四个同时拉低 ----
     * 用来区分"程序没驱动"和"灯/接线有问题": 四个一起拉低还不亮,
     * 那就是硬件侧的事。 */
    disp_clear();
    disp_printf(0, 0, "ALL PINS LOW");
    disp_printf(1, 0, "PB0 PB1 PA7 PA8");
    drive_all(1);
    HAL_Delay(PHASE_MS);

    disp_printf(0, 0, "ALL PINS HIGH");
    drive_all(0);
    HAL_Delay(PHASE_MS);

    g_dbg_loop_cnt++;
  }
}
