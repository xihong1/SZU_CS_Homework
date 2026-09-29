#ifndef __LED_H
#define __LED_H

#include "main.h"

/* ============ 引脚定义：下标 i 对应 LEDi / 掩码 bit i ============ */
#define LED_NUM             8

/* 8 路 LED 全部挂在 GPIOB 上，低电平点亮
 * 注意：PB1 已被板载 DS0 红灯占用，故 LED0 从 PB3 开始 */
#define LED0_PORT           GPIOB
#define LED0_PIN            GPIO_PIN_3

#define LED1_PORT           GPIOB
#define LED1_PIN            GPIO_PIN_4

#define LED2_PORT           GPIOB
#define LED2_PIN            GPIO_PIN_5

#define LED3_PORT           GPIOB
#define LED3_PIN            GPIO_PIN_6

#define LED4_PORT           GPIOB
#define LED4_PIN            GPIO_PIN_7

#define LED5_PORT           GPIOB
#define LED5_PIN            GPIO_PIN_8

#define LED6_PORT           GPIOB
#define LED6_PIN            GPIO_PIN_9

/* 板载 DS1 绿灯 */
#define LED7_PORT           GPIOB
#define LED7_PIN            GPIO_PIN_0

/* ============ 4 种灯效的编号 ============ */
#define EFFECT_FLOW         0   /* 特效1：单灯流水    */
#define EFFECT_DOUBLE       1   /* 特效2：双灯追逐    */
#define EFFECT_BOUNCE       2   /* 特效3：乒乓往返    */
#define EFFECT_FILL         3   /* 特效4：逐个点亮    */
#define EFFECT_NUM          4

/* ============ 对外函数 ============ */
void     led_init(void);
void     led_write(uint8_t mask);
void     effect_run(uint8_t effect, uint16_t step);
uint16_t effect_interval(uint8_t effect);

#endif /* __LED_H */
