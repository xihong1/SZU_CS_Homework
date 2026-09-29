/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    gpio.c
  * @brief   This file provides code for the configuration
  *          of all used GPIO pins.
  *
  *  说明：本文件由 STM32CubeMX 根据引脚配置自动生成。
  *        8 路 LED 的引脚（PB0、PB3~PB9）就是在 MX_GPIO_Init() 里配置的；
  *        按键和蜂鸣器的引脚则在各自的驱动文件里配置（见 key.c / beep.c）。
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "gpio.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/*----------------------------------------------------------------------------*/
/* Configure GPIO                                                             */
/*----------------------------------------------------------------------------*/
/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/** Configure pins as
        * Analog
        * Input
        * Output
        * EVENT_OUT
        * EXTI
*/
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB,
                    LED0_Pin | LED1_Pin | LED2_Pin | LED3_Pin |
                    LED4_Pin | LED5_Pin | LED6_Pin | LED7_Pin,
                    GPIO_PIN_SET);          /* 上电时输出高电平 = 全部熄灭 */

  /*Configure GPIO pins : PB0 PB3 PB4 PB5 PB6 PB7 PB8 PB9 */
  GPIO_InitStruct.Pin = LED0_Pin | LED1_Pin | LED2_Pin | LED3_Pin |
                        LED4_Pin | LED5_Pin | LED6_Pin | LED7_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

}

/* USER CODE BEGIN 2 */

/* USER CODE END 2 */
