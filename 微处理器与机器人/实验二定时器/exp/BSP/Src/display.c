/**
  ******************************************************************************
  * @file    display.c
  * @brief   统一显示接口实现 (把"行/列"翻译成 OLED 驱动的"列/页")
  ******************************************************************************
  */

#include "display.h"
#include "oled.h"
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

/* 把行号换算成 OLED 的起始页: 每行 16 像素 = 2 页 */
#define LINE_TO_PAGE(line)   ((uint8_t)((line) * 2))
#define COL_TO_X(col)        ((uint8_t)((col) * OLED_FONT_W))

void disp_init(void)
{
  OLED_Init();
  OLED_Clear();
}

void disp_clear(void)
{
  OLED_Clear();
}

/**
  * @brief  在指定位置显示字符串
  * @param  line : 0~3
  * @param  col  : 0~15
  */
void disp_str(uint8_t line, uint8_t col, const char *str)
{
  if (line >= DISP_LINE_MAX || col >= DISP_COL_MAX || str == NULL)
  {
    return;
  }
  OLED_ShowString(COL_TO_X(col), LINE_TO_PAGE(line), str);
}

/**
  * @brief  显示整数, 高位补空格
  */
void disp_int(uint8_t line, uint8_t col, int32_t val, uint8_t width)
{
  if (line >= DISP_LINE_MAX || col >= DISP_COL_MAX)
  {
    return;
  }
  OLED_ShowNum(COL_TO_X(col), LINE_TO_PAGE(line), val, width);
}

/**
  * @brief  显示整数, 高位补 0
  */
void disp_intz(uint8_t line, uint8_t col, int32_t val, uint8_t width)
{
  if (line >= DISP_LINE_MAX || col >= DISP_COL_MAX)
  {
    return;
  }
  OLED_ShowNumZ(COL_TO_X(col), LINE_TO_PAGE(line), val, width);
}

/**
  * @brief  格式化显示 (类似 printf, 但输出到 OLED)
  *         支持 %s %c %d %u %x 等, 不支持浮点
  */
void disp_printf(uint8_t line, uint8_t col, const char *fmt, ...)
{
  char     buf[64];
  va_list  args;

  if (line >= DISP_LINE_MAX || col >= DISP_COL_MAX || fmt == NULL)
  {
    return;
  }

  va_start(args, fmt);
  (void)vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);

  OLED_ShowString(COL_TO_X(col), LINE_TO_PAGE(line), buf);
}

/**
  * @brief  先写字符串, 再用空格把这一行剩下的位置填满
  *         用于消除上一次显示留下的残影(比如数字位数变少时)。
  */
void disp_str_pad(uint8_t line, uint8_t col, const char *str)
{
  uint8_t c = col;

  if (line >= DISP_LINE_MAX || col >= DISP_COL_MAX || str == NULL)
  {
    return;
  }

  while (*str != '\0' && c < DISP_COL_MAX)
  {
    OLED_ShowChar(COL_TO_X(c), LINE_TO_PAGE(line), *str);
    c++;
    str++;
  }
  while (c < DISP_COL_MAX)
  {
    OLED_ShowChar(COL_TO_X(c), LINE_TO_PAGE(line), ' ');
    c++;
  }
}
