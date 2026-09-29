/**
  ******************************************************************************
  * @file    oled.h
  * @brief   0.96 寸 OLED (SSD1306) 底层驱动 —— 8080 并口模式
  *
  * 硬件连接 (阿波罗开发板 P6 排座, OLED/CAMERA 接口, 模块靠左插):
  *     OLED_CS  -> PB7      OLED_RS  -> PB4      OLED_WR  -> PH8
  *     OLED_RD  -> PB3      OLED_RST -> PA15
  *     OLED_D0  -> PB9      OLED_D1  -> PB8      OLED_D2  -> PD3
  *     OLED_D3  -> PC11     OLED_D4  -> PC9      OLED_D5  -> PC8
  *     OLED_D6  -> PC7      OLED_D7  -> PC6
  *
  * 正点原子 OLED 模块出厂默认 BS1=BS2=VCC, 即 8080 并口方式, 不需要改焊点。
  *
  * 注意: PB3 / PB4 / PA15 复位后默认是 JTAG 的 JTDO / NJTRST / JTDI。
  *       在 STM32F4 上只要把它们配成普通 GPIO 输出即可, 不需要额外的重映射
  *       寄存器(那是 F1 才有的 AFIO_MAPR)。SWD 用的 PA13/PA14 不受影响,
  *       所以配置完成后依然可以正常调试。
  *
  * 本文件只负责"怎么把字节送到屏幕"; 面向任务的显示接口在 display.h 里。
  ******************************************************************************
  */

#ifndef __OLED_H
#define __OLED_H

#include "stm32f4xx_hal.h"

/* 屏幕参数: SSD1306, 128x64 */
#define OLED_WIDTH      128
#define OLED_HEIGHT     64
#define OLED_PAGES      8       /* 64 行 = 8 页, 每页 8 行 */

/* 字库: 8x16, 一行 16 个字符, 共 4 行 */
#define OLED_FONT_W    8
#define OLED_FONT_H    16
#define OLED_LINE_MAX  4
#define OLED_COL_MAX   16

/* ---- 底层: 命令 / 数据 ---- */
void OLED_WrCmd(uint8_t cmd);
void OLED_WrData(uint8_t dat);

/* ---- 初始化与清屏 ---- */
void OLED_Init(void);
void OLED_Clear(void);
void OLED_FillPages(uint8_t page_start, uint8_t page_end, uint8_t pattern);

/* ---- 光标与显示 ---- */
void OLED_SetCursor(uint8_t x, uint8_t page);
void OLED_ShowChar(uint8_t x, uint8_t page, char ch);
void OLED_ShowString(uint8_t x, uint8_t page, const char *str);
void OLED_ShowNum(uint8_t x, uint8_t page, int32_t num, uint8_t len);
void OLED_ShowNumZ(uint8_t x, uint8_t page, int32_t num, uint8_t len);

#endif /* __OLED_H */
