/**
  ******************************************************************************
  * @file    key.h
  * @brief   板载按键驱动 (带消抖)
  *
  * 阿波罗开发板按键:
  *     KEY0 -> PH3    低电平有效
  *     KEY1 -> PH2    低电平有效
  *     KEY2 -> PC13   低电平有效
  *     WK_UP-> PA0    高电平有效
  *
  * 按键没有外部上下拉电阻, 所以必须在芯片内部开上拉(KEY0~2)或下拉(WK_UP),
  * 否则引脚会悬空, 读到的电平不确定。
  *
  * 使用方式 (配合 1 ms 节拍):
  *     主循环里每毫秒调用一次 key_poll();
  *     想判断"按下"这个动作时用 key_take_press(), 它是边沿事件, 取走即清零,
  *     不会因为一直按着而重复触发。
  ******************************************************************************
  */

#ifndef __KEY_H
#define __KEY_H

#include "stm32f4xx_hal.h"

typedef enum
{
  KEY_0 = 0,
  KEY_1,
  KEY_2,
  KEY_UP,        /* 板上的 WK_UP 键 */
  KEY_COUNT
} key_id_t;

void    key_init(void);
void    key_poll(void);                    /* 每 1 ms 调用一次 */
uint8_t key_is_down(key_id_t k);           /* 当前是否处于按下状态(已消抖) */
uint8_t key_take_press(key_id_t k);        /* 取"按下"事件, 取走后自动清零 */

#endif /* __KEY_H */
