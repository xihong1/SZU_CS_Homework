/**
  ******************************************************************************
  * @file    stm32f4xx_hal_conf.h
  * @brief   HAL 配置头文件 (仅保留本实验用到的模块)
  *
  * 硬件: 正点原子 阿波罗 STM32F429IGT6 开发板
  *       HSE = 25 MHz, SYSCLK = 180 MHz
  ******************************************************************************
  */

#ifndef __STM32F4xx_HAL_CONF_H
#define __STM32F4xx_HAL_CONF_H

#ifdef __cplusplus
extern "C" {
#endif

/* ########################## 模块使能 #################################### */
#define HAL_MODULE_ENABLED
#define HAL_RCC_MODULE_ENABLED
#define HAL_GPIO_MODULE_ENABLED
#define HAL_EXTI_MODULE_ENABLED
#define HAL_DMA_MODULE_ENABLED
#define HAL_CORTEX_MODULE_ENABLED
#define HAL_FLASH_MODULE_ENABLED
#define HAL_PWR_MODULE_ENABLED
#define HAL_TIM_MODULE_ENABLED
#define HAL_UART_MODULE_ENABLED

/* ########################## 振荡器参数 ################################## */
#if !defined  (HSE_VALUE)
  #define HSE_VALUE              25000000U /* 阿波罗开发板外部晶振 25 MHz */
#endif

#if !defined  (HSE_STARTUP_TIMEOUT)
  #define HSE_STARTUP_TIMEOUT    100U      /* HSE 起振超时, 单位 ms */
#endif

#if !defined  (HSI_VALUE)
  #define HSI_VALUE              16000000U /* 内部高速时钟 16 MHz */
#endif

#if !defined  (LSI_VALUE)
  #define LSI_VALUE               32000U
#endif

#if !defined  (LSE_VALUE)
  #define LSE_VALUE               32768U
#endif

#if !defined  (LSE_STARTUP_TIMEOUT)
  #define LSE_STARTUP_TIMEOUT    5000U
#endif

#if !defined  (EXTERNAL_CLOCK_VALUE)
  #define EXTERNAL_CLOCK_VALUE   12288000U
#endif

/* ########################### 系统配置 ################################### */
#define  VDD_VALUE                    3300U
#define  TICK_INT_PRIORITY            0x0FU
#define  USE_RTOS                     0U
#define  PREFETCH_ENABLE              1U
#define  INSTRUCTION_CACHE_ENABLE     1U
#define  DATA_CACHE_ENABLE            1U

/* ########################## 回调注册开关 (全部关闭) ###################### */
#define  USE_HAL_UART_REGISTER_CALLBACKS        0U
#define  USE_HAL_TIM_REGISTER_CALLBACKS         0U
#define  USE_HAL_DMA_REGISTER_CALLBACKS         0U
#define  USE_HAL_RCC_REGISTER_CALLBACKS         0U
#define  USE_HAL_GPIO_REGISTER_CALLBACKS        0U
#define  USE_HAL_PWR_REGISTER_CALLBACKS         0U
#define  USE_HAL_FLASH_REGISTER_CALLBACKS       0U

/* ########################## 以太网 (未使用) ############################# */
#define MAC_ADDR0   2U
#define MAC_ADDR1   0U
#define MAC_ADDR2   0U
#define MAC_ADDR3   0U
#define MAC_ADDR4   0U
#define MAC_ADDR5   0U

/* ########################## 包含模块头文件 ############################## */
#ifdef HAL_RCC_MODULE_ENABLED
  #include "stm32f4xx_hal_rcc.h"
#endif

#ifdef HAL_GPIO_MODULE_ENABLED
  #include "stm32f4xx_hal_gpio.h"
#endif

#ifdef HAL_EXTI_MODULE_ENABLED
  #include "stm32f4xx_hal_exti.h"
#endif

#ifdef HAL_DMA_MODULE_ENABLED
  #include "stm32f4xx_hal_dma.h"
#endif

#ifdef HAL_CORTEX_MODULE_ENABLED
  #include "stm32f4xx_hal_cortex.h"
#endif

#ifdef HAL_FLASH_MODULE_ENABLED
  #include "stm32f4xx_hal_flash.h"
#endif

#ifdef HAL_PWR_MODULE_ENABLED
  #include "stm32f4xx_hal_pwr.h"
#endif

#ifdef HAL_TIM_MODULE_ENABLED
  #include "stm32f4xx_hal_tim.h"
#endif

#ifdef HAL_UART_MODULE_ENABLED
  #include "stm32f4xx_hal_uart.h"
#endif

/* ########################## 参数断言 #################################### */
/* 关闭断言以减小代码体积并提高执行速度。
 * 调试寄存器配置错误时可改为: #define assert_param(expr) ((expr) ? (void)0U : assert_failed((uint8_t *)__FILE__, __LINE__))
 */
#define assert_param(expr) ((void)0U)

#ifdef __cplusplus
}
#endif

#endif /* __STM32F4xx_HAL_CONF_H */
