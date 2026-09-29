/**
  ******************************************************************************
  * @file    gtim_pwm.h
  * @brief   通用定时器 PWM 输出驱动 —— TIM3 三路 (CH2/CH3/CH4)
  *
  * 引脚 (AF2):
  *     TIM3_CH2 -> PA7    红
  *     TIM3_CH3 -> PB0    绿
  *     TIM3_CH4 -> PB1    蓝
  *
  * 频率计算 (TIM3 挂 APB1):
  *     APB1 总线 = 180 MHz / 4 = 45 MHz
  *     预分频系数 >= 2, 所以定时器时钟 = 2 x 45 MHz = 90 MHz
  *
  *     PWM 频率 = 90 MHz / ((PSC+1)(ARR+1))
  *              = 90 MHz / (90 * 1000)
  *              = 1 kHz
  *
  * 同一定时器的多个通道共用 PSC 和 ARR, 所以三路颜色必须同频率,
  * 能各自独立调的只有 CCR(占空比)。这正是任务三要用到的性质。
  ******************************************************************************
  */

#ifndef __GTIM_PWM_H
#define __GTIM_PWM_H

#include "stm32f4xx_hal.h"

/* 三路通道编号 */
#define PWM_CH_R     0      /* TIM3_CH2 -> PA7 */
#define PWM_CH_G     1      /* TIM3_CH3 -> PB0 */
#define PWM_CH_B     2      /* TIM3_CH4 -> PB1 */
#define PWM_CH_NUM   3

/* 一个 PWM 周期对应的计数值 (ARR = 999)
 * 因此:   占空比 = CCR / PWM_PERIOD          (0.0 ~ 1.0)
 *         亮度百分比 = CCR * 100 / PWM_PERIOD */
#define PWM_PERIOD   1000U

/* PWM 频率 (Hz), 便于在报告里引用 */
#define PWM_FREQ_HZ  1000U

void     gtim_pwm_init(void);
void     gtim_pwm_set(uint8_t ch, uint16_t ccr);
uint16_t gtim_pwm_get(uint8_t ch);

/**
  * @brief  改变 PWM 频率 (只改 ARR, 保持 PSC=89 即 1 MHz 计数)
  *
  * 任务四需要用同一个定时器产生 100 Hz / 1 kHz / 10 kHz 三种信号,
  * 靠的就是改 ARR:
  *     ARR = 8999 -> 1 MHz / 9000 =  100 Hz
  *     ARR =  999 -> 1 MHz / 1000 = 1000 Hz
  *     ARR =   99 -> 1 MHz /  100 = 10 kHz
  *
  * 注意: 改完 ARR 后原来的 CCR 可能超出新周期, 调用方需要重新设置各通道占空比。
  */
void     gtim_pwm_set_period(uint16_t arr);

/* 当前一个 PWM 周期对应的计数值 (ARR + 1), 用于换算占空比 */
uint16_t gtim_pwm_period(void);

/**
  * @brief  按"亮度"设置占空比, 内部自动处理 LED 极性
  *
  * 阿波罗板载 LED 是低电平点亮 (VCC -> 限流电阻 -> LED -> GPIO),
  * 所以 PWM 高电平占的比例越大, 灯反而越暗 —— 亮度与 CCR 是反向的。
  * 这个换算统一在这里做, 上层任务只管给"亮度", 不用操心极性。
  *
  * @param  brightness : 0 ~ PWM_PERIOD, 数值越大越亮
  */
void     gtim_pwm_set_brightness(uint8_t ch, uint16_t brightness);

#endif /* __GTIM_PWM_H */
