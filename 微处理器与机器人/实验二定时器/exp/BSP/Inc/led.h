/**
  ******************************************************************************
  * @file    led.h
  * @brief   板载 LED 驱动 (LED0 = PB1 红, LED1 = PB0 绿, 低电平点亮)
  ******************************************************************************
  */

#ifndef __LED_H
#define __LED_H

#include "stm32f4xx_hal.h"

#define LED_RED     0      /* LED0, DS0, PB1 */
#define LED_GREEN   1      /* LED1, DS1, PB0 */

void led_init(void);
void led_on(uint8_t idx);
void led_off(uint8_t idx);
void led_toggle(uint8_t idx);

#endif /* __LED_H */
