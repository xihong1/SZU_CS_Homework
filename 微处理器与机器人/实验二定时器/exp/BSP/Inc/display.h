/**
  ******************************************************************************
  * @file    display.h
  * @brief   统一显示接口 —— 供各个实验任务复用的高层显示 API
  *
  * 分层结构 (对应实验要求"把底层写命令/写数据与上层文本显示分离"):
  *
  *     应用任务 (App/task_*.c)
  *          |  只使用 disp_xxx()
  *     显示接口层  display.c   <- 按"行/列"定位, 屏蔽像素与页的概念
  *          |  只使用 OLED_ShowXxx()
  *     驱动层      oled.c      <- SSD1306 命令/数据、字库、光标
  *          |  OLED_WrCmd / OLED_WrData
  *     硬件层      GPIO 软件模拟 SPI
  *
  * 上层不直接碰 OLED_WrCmd / OLED_WrData, 也不关心字符是 8x16 还是页寻址,
  * 这样以后换屏幕(比如换成 LCD)只需要改 display.c。
  *
  * 坐标约定:
  *     line : 0 ~ 3   行 (每行 16 像素高, 屏幕上共 4 行)
  *     col  : 0 ~ 15  字符列 (每列 8 像素宽, 一行共 16 个字符)
  ******************************************************************************
  */

#ifndef __DISPLAY_H
#define __DISPLAY_H

#include "stm32f4xx_hal.h"

#define DISP_LINE_MAX   4
#define DISP_COL_MAX    16

/* ---- 初始化 / 清屏 ---- */
void disp_init(void);
void disp_clear(void);

/* ---- 字符串 ---- */
void disp_str(uint8_t line, uint8_t col, const char *str);

/* ---- 整数 ---- */
void disp_int(uint8_t line, uint8_t col, int32_t val, uint8_t width);   /* 高位补空格 */
void disp_intz(uint8_t line, uint8_t col, int32_t val, uint8_t width);  /* 高位补 0   */

/* ---- 带格式的字符串 (类似 printf) ---- */
void disp_printf(uint8_t line, uint8_t col, const char *fmt, ...);

/* ---- 用字符串覆盖剩余部分, 避免旧内容残留 ---- */
void disp_str_pad(uint8_t line, uint8_t col, const char *str);

#endif /* __DISPLAY_H */
