/**
 ******************************************************************************
 * @file    led.h
 * @brief   8 路 LED 驱动（跑马灯实验）
 *
 *  8 个 LED 的分配：
 *    LED1、LED2  —— 开发板自带（DS0 红灯 = PB1，DS1 绿灯 = PB0）
 *    LED3~LED8   —— 接在面包板上的 6 个 LED
 *
 *  接线方式（每个灯都一样）：
 *      3.3V ──[1K 电阻]── LED 长脚(正极) ── LED 短脚(负极) ── 本文件的引脚
 *  因此 IO 输出低电平 = 灯亮。
 *
 *  ⚠ 注意：LED3~LED8 与蜂鸣器用的是候选引脚，接线前请对照实验箱底板的
 *     “IO 分配表”丝印确认没有被板载外设（LCD/SDRAM/NAND/网口）占用。
 *     万一被占用，只要改下面的宏定义即可，逻辑代码不用动。
 ******************************************************************************
 */
#ifndef __LED_H
#define __LED_H

#include "main.h"

/* ==================== 引脚定义（要换引脚只改这里） ==================== */
#define LED_NUM             8

/* 板载 LED：阿波罗 F429 —— DS0 红灯 = PB1，DS1 绿灯 = PB0 */
#define LED1_PORT           GPIOB
#define LED1_PIN            GPIO_PIN_1

#define LED2_PORT           GPIOB
#define LED2_PIN            GPIO_PIN_0

/* 面包板上的 6 个 LED（候选引脚，参见文件头的说明） */
#define LED3_PORT           GPIOB
#define LED3_PIN            GPIO_PIN_3

#define LED4_PORT           GPIOB
#define LED4_PIN            GPIO_PIN_4

#define LED5_PORT           GPIOB
#define LED5_PIN            GPIO_PIN_5

#define LED6_PORT           GPIOB
#define LED6_PIN            GPIO_PIN_6

#define LED7_PORT           GPIOB
#define LED7_PIN            GPIO_PIN_7

#define LED8_PORT           GPIOB
#define LED8_PIN            GPIO_PIN_9

/* ==================== 4 种灯效的编号 ==================== */
#define EFFECT_FLOW         0   /* 特效1：单灯流水 */
#define EFFECT_DOUBLE       1   /* 特效2：双灯追逐 */
#define EFFECT_BOUNCE       2   /* 特效3：乒乓往返 */
#define EFFECT_FILL         3   /* 特效4：逐个点亮再熄灭 */
#define EFFECT_NUM          4

/* ==================== 对外函数 ==================== */
void     led_init(void);
void     led_write(uint8_t mask);
void     effect_run(uint8_t effect, uint16_t step);
uint16_t effect_interval(uint8_t effect);

#endif /* __LED_H */
