/**
  ******************************************************************************
  * @file    gtim_ic.c
  * @brief   TIM1_CH1 输入捕获, PWM 输入模式 (PA8)
  *
  * 接线:  PB1 (TIM3_CH4, PWM 输出)  ──跳线──  PA8 (TIM1_CH1, 捕获输入)
  *
  * 为什么不用 TIM5/PA0 或 TIM5/PA1:
  *     开发指南的输入捕获例子用的是 TIM5_CH1/PA0, 但本板实测 PA0 与排针上
  *     实际可接的位置对不上; 换到 PA1(TIM5_CH2) 后从模式触发又始终把计数器
  *     压在 0, 排查成本很高。
  *     PA8 是确定引出的引脚(上面接着 LED), 且 TIM1_CH1 是标准的 AF1,
  *     所以改用 PA8 最稳妥。
  *
  * 时钟: TIM1 挂 APB2
  *     APB2 总线 = 180 MHz / 2 = 90 MHz
  *     预分频系数 >= 2, 所以定时器时钟 = 2 x 90 MHz = 180 MHz
  *     PSC = 35 -> 180 MHz / 36 = 5 MHz, 分辨率 0.2 us
  *
  * 注意: TIM1 是 **16 位** 定时器, ARR 最大只能到 65535。
  *       所以捕获时钟不能取太高: 100 Hz 的周期是 10 ms, 若用 10 MHz 计数
  *       需要 100000 个计数, 已经超过 65535 会溢出。取 5 MHz 则只要 50000,
  *       留出了余量。(TIM2/TIM5 才是 32 位, 但它们的可用引脚在本板上对不上)
  ******************************************************************************
  */

#include "gtim_ic.h"

/* TIM1 寄存器位定义 (避开 HAL 头文件里已占用的 TIM_xxx 名字) */
#define GTIM_CC1S_POS      0      /* CCMR1 : CC1S[1:0]   IC1 输入映射 */
#define GTIM_CC2S_POS      8      /* CCMR1 : CC2S[1:0]   IC2 输入映射 */
#define GTIM_CC1E          (1U << 0)      /* CCER : CH1 捕获使能   */
#define GTIM_CC1P          (1U << 1)      /* CCER : CH1 触发极性   */
#define GTIM_CC2E          (1U << 4)      /* CCER : CH2 捕获使能   */
#define GTIM_CC2P          (1U << 5)      /* CCER : CH2 触发极性   */
#define GTIM_TS_TI1FP1     (5U << 4)      /* SMCR : 触发源 = TI1FP1 */
#define GTIM_SMS_RESET     (4U << 0)      /* SMCR : 复位模式        */

#define GTIM_TIM          TIM1
#define GTIM_PSC          35U             /* 180 MHz / 36 = 5 MHz */
#define GTIM_GPIO_PORT    GPIOA
#define GTIM_GPIO_PIN     GPIO_PIN_8
#define GTIM_GPIO_AF      GPIO_AF1_TIM1

/* ==========================================================================
 * 初始化
 * ========================================================================== */
void gtim_ic_init(void)
{
  GPIO_InitTypeDef gpio = {0};

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_TIM1_CLK_ENABLE();

  /* ---- PA8 -> TIM1_CH1 (AF1) ----
   * 用内部下拉: 拔掉跳线后输入被拉到低电平, 不会因为悬空拾取噪声
   * 产生假边沿, "无信号"才能判断得稳定可靠。 */
  gpio.Mode      = GPIO_MODE_AF_PP;
  gpio.Pull      = GPIO_PULLDOWN;
  gpio.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
  gpio.Alternate = GTIM_GPIO_AF;
  gpio.Pin       = GTIM_GPIO_PIN;
  HAL_GPIO_Init(GTIM_GPIO_PORT, &gpio);

  /* ---- 时基: 10 MHz 计数, 32 位周期 ---- */
  GTIM_TIM->CR1  = 0;                   /* 先停机再配置 */
  GTIM_TIM->PSC  = GTIM_PSC;
  GTIM_TIM->ARR  = 0xFFFFU;             /* 16 位定时器, 这就是最大值 */
  GTIM_TIM->CNT  = 0;

  /* ---- PWM 输入模式 ----
   * CC1S = 01: IC1 映射到 TI1 (直接通道) —— 负责捕上升沿并复位计数器
   * CC2S = 10: IC2 也映射到 TI1 (间接通道) —— 负责捕下降沿
   * 两个通道读同一个引脚, 一路信号就能同时量出周期和高电平时间。 */
  GTIM_TIM->CCMR1 = (1U << GTIM_CC1S_POS) | (2U << GTIM_CC2S_POS);

  /* CC1 捕上升沿, CC2 捕下降沿 */
  GTIM_TIM->CCER  = GTIM_CC1E | GTIM_CC2E | GTIM_CC2P;

  /* 从模式: 触发源 TI1FP1, 复位模式
   * 每来一个上升沿就把 CNT 清零, 所以 CCR1 里存下的正好是一个完整周期的
   * 计数值, CCR2 里是上升沿到下降沿(高电平)的计数值。 */
  GTIM_TIM->SMCR  = GTIM_TS_TI1FP1 | GTIM_SMS_RESET;

  GTIM_TIM->CCR1 = 0;
  GTIM_TIM->CCR2 = 0;
  GTIM_TIM->SR   = 0;

  /* 不开捕获中断: 每个边沿都进中断的话, 高速信号下 CPU 会一直被困在中断里
   * (初始化都走不完)。反正我们只需要知道"信号还在不在", 用轮询就够了。 */

  GTIM_TIM->CR1 |= (1U << 0);           /* CEN = 1, 启动计数 */
}

/* ==========================================================================
 * 读取测量结果
 * ========================================================================== */
uint8_t gtim_ic_read(uint32_t *period, uint32_t *high)
{
  uint32_t p1 = GTIM_TIM->CCR1;     /* 周期 */
  uint32_t h  = GTIM_TIM->CCR2;     /* 高电平 */
  uint32_t p2 = GTIM_TIM->CCR1;

  if (p1 == 0U)                     /* 还没捕到信号 */
  {
    return 0;
  }

  if (p1 != p2)                     /* 期间有新捕获, 这组数据跨周期了, 丢弃 */
  {
    return 0;
  }

  if (h > p1)                       /* 高电平不可能超过一个周期 */
  {
    return 0;
  }

  *period = p1;
  *high   = h;
  return 1;
}
