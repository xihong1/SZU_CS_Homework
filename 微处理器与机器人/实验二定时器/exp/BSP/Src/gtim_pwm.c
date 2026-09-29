/**
  ******************************************************************************
  * @file    gtim_pwm.c
  * @brief   通用定时器 TIM3 三路 PWM 输出
  ******************************************************************************
  */

#include "gtim_pwm.h"
#include "main.h"
#include "app_config.h"

static TIM_HandleTypeDef s_htim3;

/* 当前一个 PWM 周期对应的计数值 (ARR + 1)。
 * 任务四会改 ARR 来切换频率, 所以占空比换算不能写死成 PWM_PERIOD。 */
static uint16_t s_period = PWM_PERIOD;

/* 通道编号 -> HAL 通道宏 */
static const uint32_t s_channel[PWM_CH_NUM] =
{
  TIM_CHANNEL_2,     /* 红 PA7 */
  TIM_CHANNEL_3,     /* 绿 PB0 */
  TIM_CHANNEL_4,     /* 蓝 PB1 */
};

/* ==========================================================================
 * 初始化
 * ========================================================================== */
void gtim_pwm_init(void)
{
  GPIO_InitTypeDef  gpio = {0};
  TIM_OC_InitTypeDef oc  = {0};

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_TIM3_CLK_ENABLE();

  /* ---- 1. 把三个引脚配成定时器复用输出 ----
   * 必须是 AF_PP(复用推挽), 不能是普通 GPIO 输出:
   * 只有复用模式下, PWM 信号才会从定时器直接连到引脚。
   * TIM3 在 STM32F429 上对应 AF2。 */
  gpio.Mode      = GPIO_MODE_AF_PP;
  gpio.Pull      = GPIO_NOPULL;
  gpio.Speed     = GPIO_SPEED_FREQ_HIGH;
  gpio.Alternate = GPIO_AF2_TIM3;

  gpio.Pin = GPIO_PIN_7;                        /* PA7 -> CH2 */
  HAL_GPIO_Init(GPIOA, &gpio);

  gpio.Pin = GPIO_PIN_0 | GPIO_PIN_1;           /* PB0 -> CH3, PB1 -> CH4 */
  HAL_GPIO_Init(GPIOB, &gpio);

  /* ---- 2. 时基: 1 kHz ----
   * 90 MHz / (89+1) = 1 MHz 计数时钟
   * 1 MHz / (999+1) = 1 kHz, 即 PWM 周期 1 ms */
  s_htim3.Instance               = TIM3;
  s_htim3.Init.Prescaler         = 89;
  s_htim3.Init.CounterMode       = TIM_COUNTERMODE_UP;
  s_htim3.Init.Period            = 999;
  s_htim3.Init.ClockDivision     = TIM_CLOCKDIVISION_DIV1;
  s_htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;

  if (HAL_TIM_PWM_Init(&s_htim3) != HAL_OK)
  {
    Error_Handler();
  }

  /* ---- 3. 三个通道都配成 PWM 模式 1 ----
   * PWM 模式 1: 计数值 CNT < CCR 时输出有效电平, 也就是说
   *             CCR 越大, 高电平占的比例越大, 低电平点亮的 LED 就越暗。
   * 初始 CCR = 0, 上电时三路都是全灭状态, 不会闪一下。 */
  oc.OCMode       = TIM_OCMODE_PWM1;
  oc.Pulse        = 0;
  oc.OCPolarity   = TIM_OCPOLARITY_HIGH;
  oc.OCFastMode   = TIM_OCFAST_DISABLE;
  oc.OCIdleState  = TIM_OCIDLESTATE_RESET;

  for (uint8_t i = 0; i < PWM_CH_NUM; i++)
  {
    if (HAL_TIM_PWM_ConfigChannel(&s_htim3, &oc, s_channel[i]) != HAL_OK)
    {
      Error_Handler();
    }
    if (HAL_TIM_PWM_Start(&s_htim3, s_channel[i]) != HAL_OK)
    {
      Error_Handler();
    }
  }
}

/* ==========================================================================
 * 设置 / 读取占空比
 *
 * CCR 一旦写入就立刻生效(ARPE=1 只影响 ARR 的更新时机)。
 * 如果改用带预装载的 CCR, 新的占空比会在下一个更新事件才生效,
 * 能彻底避免周期中间改 CCR 造成的毛刺。
 * ========================================================================== */
void gtim_pwm_set(uint8_t ch, uint16_t ccr)
{
  if (ch >= PWM_CH_NUM)
  {
    return;
  }
  if (ccr > s_period)          /* CCR = period 即 100% 占空比 */
  {
    ccr = s_period;
  }
  __HAL_TIM_SET_COMPARE(&s_htim3, s_channel[ch], ccr);
}

/**
  * @brief  改变 PWM 频率 (只改 ARR)
  *
  * ARPE = 1, 所以新 ARR 会在下一个更新事件才真正生效, 不会在周期中间
  * 突然截断当前周期。代价是切换频率后头一个周期可能还是旧的, 对测量无影响。
  */
void gtim_pwm_set_period(uint16_t arr)
{
  __HAL_TIM_SET_AUTORELOAD(&s_htim3, arr);
  s_period = (uint16_t)(arr + 1U);
}

uint16_t gtim_pwm_period(void)
{
  return s_period;
}

uint16_t gtim_pwm_get(uint8_t ch)
{
  if (ch >= PWM_CH_NUM)
  {
    return 0;
  }
  return (uint16_t)__HAL_TIM_GET_COMPARE(&s_htim3, s_channel[ch]);
}

/**
  * @brief  按亮度设置, 自动处理 LED 极性
  *
  * 低电平点亮的 LED:
  *     亮度 0    -> CCR = 1000 -> 输出恒高 -> 灯全灭
  *     亮度 1000 -> CCR = 0    -> 输出恒低 -> 灯全亮
  * 也就是 CCR = PWM_PERIOD - 亮度  (反相)
  */
void gtim_pwm_set_brightness(uint8_t ch, uint16_t brightness)
{
  if (brightness > PWM_PERIOD)
  {
    brightness = PWM_PERIOD;
  }

#if LED_ACTIVE_LOW
  gtim_pwm_set(ch, (uint16_t)(PWM_PERIOD - brightness));
#else
  gtim_pwm_set(ch, brightness);
#endif
}
