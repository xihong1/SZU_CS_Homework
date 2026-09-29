/**
  ******************************************************************************
  * @file    main.h
  * @brief   全局公共声明
  ******************************************************************************
  */

#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f4xx_hal.h"

/**
  * @brief  初始化失败时的兜底处理 (定义在 main.c)
  *         关中断后死循环, 便于用调试器看现场。
  */
void Error_Handler(void);

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
