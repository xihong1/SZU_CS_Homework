/**
  ******************************************************************************
  * @file    main.c
  * @brief   微处理器与机器人实验二 —— 定时器实验
  *
  * 硬件: 正点原子 阿波罗 STM32F429IGT6 开发板 + ATK DAP 仿真器
  * 时钟: HSE 25 MHz -> PLL -> SYSCLK 180 MHz
  *
  * 本文件只负责三件事:
  *     1) 配置系统时钟树
  *     2) 初始化板上公共外设 (LED / OLED 显示)
  *     3) 根据 APP_TASK 选一个实验任务跑起来
  * 具体任务逻辑都在 App/Src/taskX_*.c 里。
  ******************************************************************************
  */

#include "stm32f4xx_hal.h"
#include "app_config.h"
#include "app_debug.h"
#include "led.h"
#include "display.h"
#include "tick.h"
#include "key.h"

#include "task1_oled.h"
#include "task2_reaction.h"
#include "task3_breath.h"
#include "task4_freqmeter.h"
#include "debug_led.h"

/* ==========================================================================
 * 选择要运行的任务
 *     0 = LED 接线自检        (调试用, 不参与实验评分)
 *     1 = 任务一 OLED 基础显示
 *     2 = 任务二 随机反应速度测试器
 *     3 = 任务三 三色流水呼吸灯
 *     4 = 任务四 频率与占空比自测仪
 *     5 = 任务五 N 次闪光与硬件急停
 * ========================================================================== */
#define APP_TASK   4

/* ==========================================================================
 * 调试变量 (声明见 app_debug.h, 可用 pyOCD 回读)
 * ========================================================================== */
volatile uint32_t g_dbg_boot_magic  = 0;
volatile uint32_t g_dbg_last_state  = 0;
volatile uint32_t g_dbg_systick_cnt = 0;
volatile uint32_t g_dbg_loop_cnt    = 0;
volatile uint32_t g_dbg_led_toggles = 0;
volatile uint32_t g_fault_flags     = 0;

/* 执行阶段标记, 卡在哪一步一眼就能看出来 */
#define STAGE_START       0xA1UL
#define STAGE_CLOCK_OK    0xA2UL
#define STAGE_GPIO_OK     0xA3UL
#define STAGE_OLED_OK     0xA4UL
#define STAGE_LOOP        0xA5UL

/* 时钟配置内部的失败点 */
#define ERR_CLK_TO_HSI    0x100UL
#define ERR_OSC_CONFIG    0x101UL
#define ERR_OVERDRIVE     0x102UL
#define ERR_CLK_CONFIG    0x103UL

static void SystemClock_Config(void);
static void Error_Handler_LED(uint32_t code);

/* ==========================================================================
 * main
 * ========================================================================== */
int main(void)
{
  HAL_Init();

  g_dbg_boot_magic = DBG_BOOT_MAGIC;
  g_dbg_last_state = STAGE_START;

  SystemClock_Config();
  g_dbg_last_state = STAGE_CLOCK_OK;

  led_init();
  g_dbg_last_state = STAGE_GPIO_OK;

  disp_init();
  g_dbg_last_state = STAGE_OLED_OK;

  g_dbg_last_state = STAGE_LOOP;

#if   APP_TASK == 0
  debug_led_run();

#elif APP_TASK == 1
  task1_run();

#elif APP_TASK == 2
  tick_init();
  key_init();
  task2_run();

#elif APP_TASK == 3
  tick_init();
  key_init();
  task3_run();

#elif APP_TASK == 4
  tick_init();
  key_init();
  task4_run();

#else
#error "APP_TASK 选择了尚未实现的任务"
#endif
}

/* ==========================================================================
 * 系统时钟: HSE 25 MHz -> SYSCLK 180 MHz
 *
 *   VCO 输入 = HSE / PLLM    = 25 MHz / 25     = 1 MHz
 *   VCO 输出 = VCO 输入 * PLLN = 1 MHz * 360    = 360 MHz
 *   SYSCLK   = VCO 输出 / PLLP = 360 MHz / 2    = 180 MHz
 *
 *   AHB  = SYSCLK / 1 = 180 MHz
 *   APB1 = AHB / 4    =  45 MHz
 *   APB2 = AHB / 2    =  90 MHz
 *
 * APB1/APB2 的分频系数都 >= 2, 所以挂在其上的定时器时钟是对应 APB 时钟的 2 倍:
 *     挂 APB1 的定时器 (TIM2~7, TIM12~14) ->  90 MHz
 *     挂 APB2 的定时器 (TIM1, TIM8~11)    -> 180 MHz
 *
 * 这个换算直接决定了所有定时器的 PSC/ARR 取值, 后面每个任务都要用到。
 * ========================================================================== */
static void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /* ---- 0a. 打开 PWR 外设时钟 ----
   * 不开 PWR 时钟的话, 对 PWR_CR/PWR_CSR 的读写全部无效,
   * HAL_PWREx_EnableOverDrive() 会等不到 ODRDY 而超时返回。 */
  __HAL_RCC_PWR_CLK_ENABLE();

  /* ---- 0b. 先把系统时钟切回 HSI, 保证从一个确定的状态开始 ----
   * 正常复位后 SYSCLK 就是 HSI, 这里什么都不会做。
   * 但如果程序是被调试器从 Bootloader 手里接管过来的, SYSCLK 可能已经是 PLL,
   * 那样 HAL_RCC_OscConfig 内部会走"PLL 已作系统时钟则跳过 HSE 配置"的分支,
   * 接着去关 PLL 时就会失败 —— 因为 PLL 正在驱动系统时钟。 */
  if (__HAL_RCC_GET_SYSCLK_SOURCE() != RCC_CFGR_SWS_HSI)
  {
    RCC_ClkInitStruct.ClockType      = RCC_CLOCKTYPE_SYSCLK;
    RCC_ClkInitStruct.SYSCLKSource   = RCC_SYSCLKSOURCE_HSI;
    RCC_ClkInitStruct.AHBCLKDivider  = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
    {
      Error_Handler_LED(ERR_CLK_TO_HSI);
    }
  }

  /* ---- 1. HSE + PLL ---- */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState       = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState   = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource  = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM       = 25;
  RCC_OscInitStruct.PLL.PLLN       = 360;
  RCC_OscInitStruct.PLL.PLLP       = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ       = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler_LED(ERR_OSC_CONFIG);
  }

  /* ---- 2. Over-Drive: 180 MHz 必须开启 ---- */
  if (HAL_PWREx_EnableOverDrive() != HAL_OK)
  {
    Error_Handler_LED(ERR_OVERDRIVE);
  }

  /* ---- 3. 总线分频 + Flash 等待周期 (180 MHz 需要 5 个等待周期) ---- */
  RCC_ClkInitStruct.ClockType      = RCC_CLOCKTYPE_HCLK   | RCC_CLOCKTYPE_SYSCLK |
                                     RCC_CLOCKTYPE_PCLK1  | RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource   = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider  = RCC_SYSCLK_DIV1;   /* HCLK  = 180 MHz */
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;     /* PCLK1 =  45 MHz */
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;     /* PCLK2 =  90 MHz */
  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler_LED(ERR_CLK_CONFIG);
  }
}

/* ==========================================================================
 * 出错处理: 记录失败点 + 快闪 LED
 * ========================================================================== */
static void Error_Handler_LED(uint32_t code)
{
  g_dbg_last_state = code;

  led_init();

  while (1)
  {
    led_toggle(LED_RED);
    for (volatile uint32_t i = 0; i < 200000; i++) { __NOP(); }
  }
}

void Error_Handler(void)
{
  __disable_irq();
  while (1) { }
}
