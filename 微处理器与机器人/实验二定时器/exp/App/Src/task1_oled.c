/**
  ******************************************************************************
  * @file    task1_oled.c
  * @brief   任务一: OLED 基础显示
  ******************************************************************************
  */

#include "task1_oled.h"
#include "app_config.h"
#include "app_debug.h"
#include "display.h"
#include "led.h"

void task1_run(void)
{
  uint32_t counter = 0;

  disp_clear();

  /* 静态信息: 实验名称 / 姓名 / 学号 */
  disp_str(0, 0, "Exp2: Timer");
  disp_printf(1, 0, "Name: %s", STUDENT_NAME);
  disp_printf(2, 0, "ID  : %s", STUDENT_ID);
  disp_str(3, 0, "Count:");

  while (1)
  {
    /* 动态更新的递增计数值。
     * 用定宽补零显示, 位数不会变化, 所以不会残留上一次的旧字符。 */
    disp_intz(3, 7, (int32_t)counter, 6);
    counter++;

    g_dbg_loop_cnt++;
    led_toggle(LED_RED);          /* 板载红灯做运行指示 */

    HAL_Delay(500);
  }
}
