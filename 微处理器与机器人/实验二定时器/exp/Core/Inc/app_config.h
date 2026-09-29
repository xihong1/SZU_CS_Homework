/**
  ******************************************************************************
  * @file    app_config.h
  * @brief   实验个人信息与全局配置
  *
  *  >>> 请把下面两行改成你自己的姓名和学号 <<<
  *      改完重新 make && make flash 即可。
  ******************************************************************************
  */

#ifndef __APP_CONFIG_H
#define __APP_CONFIG_H

/* ====== 学生信息 (提交报告前请填写) ====== */
/* 姓名用拼音缩写即可直接显示 —— 8x16 字库只覆盖 ASCII,
 * 中文需要额外的 16x16 汉字点阵字库才能显示。 */
#define STUDENT_NAME    "drl"
#define STUDENT_ID      "2024150040"
#define EXP_NAME        "Exp2 Timer"

/* ====== LED 极性 ======
 * 1 = 低电平点亮: 电路是 VCC -> 限流电阻 -> LED -> GPIO, GPIO 拉低才有电流。
 *     阿波罗板载 LED 就是这个接法, 外接 LED 如果也照这个接法, 保持一致。
 * 0 = 高电平点亮: GPIO -> 限流电阻 -> LED -> GND。
 *
 * 这个宏决定 PWM 占空比和亮度的对应方向: 极性搞反的话,
 * "呼吸"会变成"越调越暗", 所以两个任务(三色呼吸灯、N次闪光)都依赖它。 */
#define LED_ACTIVE_LOW   1

/* ====== 板载 LED ======
 * 阿波罗开发板: LED0 = PB1 (DS0 红), LED1 = PB0 (DS1 绿), 均为低电平点亮 */
#define LED0_GPIO_PORT  GPIOB
#define LED0_GPIO_PIN   GPIO_PIN_1
#define LED1_GPIO_PORT  GPIOB
#define LED1_GPIO_PIN   GPIO_PIN_0

/* ====== 板载按键 ======
 * KEY0/KEY1/KEY2 按下为低电平; WK_UP 按下为高电平 */
#define KEY0_GPIO_PORT  GPIOH
#define KEY0_GPIO_PIN   GPIO_PIN_3
#define KEY1_GPIO_PORT  GPIOH
#define KEY1_GPIO_PIN   GPIO_PIN_2
#define KEY2_GPIO_PORT  GPIOC
#define KEY2_GPIO_PIN   GPIO_PIN_13
#define WKUP_GPIO_PORT  GPIOA
#define WKUP_GPIO_PIN   GPIO_PIN_0

#endif /* __APP_CONFIG_H */
