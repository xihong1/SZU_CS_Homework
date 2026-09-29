/**
  ******************************************************************************
  * @file    oled.c
  * @brief   0.96 寸 OLED (SSD1306) 底层驱动 —— 8080 并口模式
  *
  * 正点原子 OLED 模块出厂默认 BS1=BS2=VCC, 即 8080 并口方式,
  * 与阿波罗开发板 P6 排座 (OLED/CAMERA 接口) 直接对插即可, 靠左插。
  *
  * 引脚对应 (来自《阿波罗开发板指南》第 23.2 节):
  *     OLED_CS   -> PB7     (DCMI_VSYNC)
  *     OLED_RS   -> PB4     (DCMI_SCL)
  *     OLED_WR   -> PH8     (DCMI_HREF)
  *     OLED_RD   -> PB3     (DCMI_SDA)
  *     OLED_RST  -> PA15    (DCMI_RESET)
  *     OLED_D0   -> PC6      OLED_D4   -> PC11
  *     OLED_D1   -> PC7      OLED_D5   -> PD3
  *     OLED_D2   -> PC8      OLED_D6   -> PB8
  *     OLED_D3   -> PC9      OLED_D7   -> PB9
  *
  * 数据总线 D0~D7 不是连在同一个端口上, 而是散在 GPIOB / GPIOC / GPIOD 三个
  * 端口里, 所以写一个字节要分三次 BSRR 操作拼出来(见 oled_bus_write)。
  *
  * 8080 写时序 (指南 23.1.1 节):
  *     RS 置成命令/数据 -> CS 拉低 -> WR 拉低准备 -> 数据送上 D[7:0]
  *     -> WR 拉高, 上升沿把数据锁进 SSD1306 -> CS 拉高
  *
  * 注意: PB3 / PB4 / PA15 复位后默认是 JTAG 的 JTDO / NJTRST / JTDI,
  *       在 STM32F4 上配成普通 GPIO 输出即可(不需要 F1 那种 AFIO 重映射)。
  *       SWD 用的 PA13/PA14 不受影响, 配完依然能正常调试。
  ******************************************************************************
  */

#include "oled.h"
#include "oledfont.h"

/* ==========================================================================
 * 控制线
 * ========================================================================== */
#define OLED_CS_PORT    GPIOB
#define OLED_CS_PIN     GPIO_PIN_7

#define OLED_RS_PORT    GPIOB
#define OLED_RS_PIN     GPIO_PIN_4

#define OLED_WR_PORT    GPIOH
#define OLED_WR_PIN     GPIO_PIN_8

#define OLED_RD_PORT    GPIOB
#define OLED_RD_PIN     GPIO_PIN_3

#define OLED_RST_PORT   GPIOA
#define OLED_RST_PIN    GPIO_PIN_15

/* 数据线: 端口 + 位号
 *
 * 指南 23.2 节写的是 "OLED_D[7:0]对应 DCMI_D[7:0]，即：PB9/PB8/PD3/PC11/PC9/PC8/PC7/PC6"。
 * 注意 D[7:0] 是降序记法, 这份列表是按 D7 -> D0 排的, 千万不要顺着读成 D0->D7。
 * 对照 STM32F429 的标准 DCMI 复用映射即可确认:
 *     DCMI_D0 = PC6    DCMI_D4 = PC11
 *     DCMI_D1 = PC7    DCMI_D5 = PD3
 *     DCMI_D2 = PC8    DCMI_D6 = PB8
 *     DCMI_D3 = PC9    DCMI_D7 = PB9
 */
#define OLED_D0_PORT    GPIOC
#define OLED_D0_BIT     6
#define OLED_D1_PORT    GPIOC
#define OLED_D1_BIT     7
#define OLED_D2_PORT    GPIOC
#define OLED_D2_BIT     8
#define OLED_D3_PORT    GPIOC
#define OLED_D3_BIT     9
#define OLED_D4_PORT    GPIOC
#define OLED_D4_BIT     11
#define OLED_D5_PORT    GPIOD
#define OLED_D5_BIT     3
#define OLED_D6_PORT    GPIOB
#define OLED_D6_BIT     8
#define OLED_D7_PORT    GPIOB
#define OLED_D7_BIT     9

/* 用 BSRR 置位/复位: 低 16 位写 1 是置位, 高 16 位写 1 是复位 */
#define OLED_CS_L()     (OLED_CS_PORT->BSRR  = (uint32_t)OLED_CS_PIN  << 16)
#define OLED_CS_H()     (OLED_CS_PORT->BSRR  = (uint32_t)OLED_CS_PIN)
#define OLED_RS_L()     (OLED_RS_PORT->BSRR  = (uint32_t)OLED_RS_PIN  << 16)
#define OLED_RS_H()     (OLED_RS_PORT->BSRR  = (uint32_t)OLED_RS_PIN)
#define OLED_WR_L()     (OLED_WR_PORT->BSRR  = (uint32_t)OLED_WR_PIN  << 16)
#define OLED_WR_H()     (OLED_WR_PORT->BSRR  = (uint32_t)OLED_WR_PIN)
#define OLED_RD_L()     (OLED_RD_PORT->BSRR  = (uint32_t)OLED_RD_PIN  << 16)
#define OLED_RD_H()     (OLED_RD_PORT->BSRR  = (uint32_t)OLED_RD_PIN)
#define OLED_RST_L()    (OLED_RST_PORT->BSRR = (uint32_t)OLED_RST_PIN << 16)
#define OLED_RST_H()    (OLED_RST_PORT->BSRR = (uint32_t)OLED_RST_PIN)

/* ==========================================================================
 * 把一字节送上打散的数据总线
 *
 * 按端口分三次写 BSRR:
 *     GPIOB 管 D0(PB9), D1(PB8)
 *     GPIOC 管 D3(PC11), D4(PC9), D5(PC8), D6(PC7), D7(PC6)
 *     GPIOD 管 D2(PD3)
 * 每个 bit 都同时给出"置位"和"复位"两种写法, 一次写完不用读改写。
 * ========================================================================== */
static inline void oled_bus_write(uint8_t dat)
{
  /* GPIOB 管 D6(PB8), D7(PB9) */
  GPIOB->BSRR =
      (((dat & 0x40) ? (1UL << OLED_D6_BIT) : (1UL << (OLED_D6_BIT + 16)))) |
      (((dat & 0x80) ? (1UL << OLED_D7_BIT) : (1UL << (OLED_D7_BIT + 16))));

  /* GPIOC 管 D0(PC6), D1(PC7), D2(PC8), D3(PC9), D4(PC11) */
  GPIOC->BSRR =
      (((dat & 0x01) ? (1UL << OLED_D0_BIT) : (1UL << (OLED_D0_BIT + 16)))) |
      (((dat & 0x02) ? (1UL << OLED_D1_BIT) : (1UL << (OLED_D1_BIT + 16)))) |
      (((dat & 0x04) ? (1UL << OLED_D2_BIT) : (1UL << (OLED_D2_BIT + 16)))) |
      (((dat & 0x08) ? (1UL << OLED_D3_BIT) : (1UL << (OLED_D3_BIT + 16)))) |
      (((dat & 0x10) ? (1UL << OLED_D4_BIT) : (1UL << (OLED_D4_BIT + 16))));

  /* GPIOD 管 D5(PD3) */
  GPIOD->BSRR =
      (((dat & 0x20) ? (1UL << OLED_D5_BIT) : (1UL << (OLED_D5_BIT + 16))));
}

/* ==========================================================================
 * 并口时序延时
 *
 * 内核 180 MHz, 一个周期约 5.6 ns。24 个 NOP 约 133 ns, 足以满足
 * SSD1306 8080 接口的时序要求:
 *     t_AS  (RS/CS 建立)       >= 15 ns
 *     t_DSW (数据建立, WR 上升前) >= 40 ns
 *     t_DHW (数据保持, WR 上升后) >= 15 ns
 *     WR 低电平宽度            >= 50 ns
 *
 * 注意: 直接把数据写上去就立刻抬高 WR 是不行的 —— 那样数据建立时间
 *       只有十来个 ns, SSD1306 可能锁存到错误的值, 表现就是全黑或花屏。
 * ========================================================================== */
#define OLED_DELAY()  do {                                                     \
    __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP();    \
    __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP();    \
    __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP();    \
  } while (0)

/* ==========================================================================
 * 8080 并口写: is_data = 0 写命令, 1 写数据
 *
 * 时序: RS 置命令/数据 -> CS 拉低 -> WR 拉低 -> 数据上总线
 *       -> WR 拉高(上升沿锁存) -> CS 拉高
 * ========================================================================== */
static inline void oled_wr(uint8_t dat, uint8_t is_data)
{
  if (is_data)
  {
    OLED_RS_H();
  }
  else
  {
    OLED_RS_L();
  }

  OLED_CS_L();
  OLED_DELAY();             /* t_AS: 让 RS/CS 先稳定 */

  OLED_WR_L();
  OLED_DELAY();             /* WR 低电平宽度 */

  oled_bus_write(dat);      /* 数据送上总线 */
  OLED_DELAY();             /* t_DSW: 关键! 让数据在 WR 上升前沿稳定下来 */

  OLED_WR_H();              /* WR 上升沿: SSD1306 在此刻锁存 */
  OLED_DELAY();             /* t_DHW: 数据保持 */

  OLED_CS_H();
}

void OLED_WrCmd(uint8_t cmd)
{
  oled_wr(cmd, 0);
}

void OLED_WrData(uint8_t dat)
{
  oled_wr(dat, 1);
}

/* ==========================================================================
 * GPIO 初始化
 * ========================================================================== */
static void oled_gpio_init(void)
{
  GPIO_InitTypeDef gpio = {0};

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();

  /* 先把控制线都置成无效电平, 避免配置过程中送出毛刺 */
  OLED_CS_H();
  OLED_RS_H();
  OLED_WR_H();
  OLED_RD_H();              /* RD 全程保持高(不读), 否则会干扰写时序 */
  OLED_RST_H();

  gpio.Mode  = GPIO_MODE_OUTPUT_PP;
  gpio.Pull  = GPIO_NOPULL;
  gpio.Speed = GPIO_SPEED_FREQ_VERY_HIGH;

  gpio.Pin = OLED_CS_PIN;                 /* PB7 */
  HAL_GPIO_Init(OLED_CS_PORT, &gpio);

  gpio.Pin = OLED_RS_PIN;                 /* PB4 */
  HAL_GPIO_Init(OLED_RS_PORT, &gpio);

  gpio.Pin = OLED_RD_PIN;                 /* PB3 */
  HAL_GPIO_Init(OLED_RD_PORT, &gpio);

  gpio.Pin = OLED_WR_PIN;                 /* PH8 */
  HAL_GPIO_Init(OLED_WR_PORT, &gpio);

  gpio.Pin = OLED_RST_PIN;                /* PA15 */
  HAL_GPIO_Init(OLED_RST_PORT, &gpio);

  /* 数据线 D0~D7 */
  gpio.Pin = GPIO_PIN_8 | GPIO_PIN_9;                             /* D6=PB8, D7=PB9 */
  HAL_GPIO_Init(GPIOB, &gpio);

  gpio.Pin = GPIO_PIN_6 | GPIO_PIN_7 | GPIO_PIN_8 |
             GPIO_PIN_9 | GPIO_PIN_11;                            /* D0~D4 = PC6,PC7,PC8,PC9,PC11 */
  HAL_GPIO_Init(GPIOC, &gpio);

  gpio.Pin = GPIO_PIN_3;                                          /* D5 = PD3 */
  HAL_GPIO_Init(GPIOD, &gpio);

  oled_bus_write(0x00);
}

/* ==========================================================================
 * 初始化: 复位时序 + SSD1306 命令序列
 * ========================================================================== */
void OLED_Init(void)
{
  oled_gpio_init();

  /* ---- 硬复位: RST 低 -> 高 ---- */
  OLED_RST_L();
  HAL_Delay(20);
  OLED_RST_H();
  HAL_Delay(20);

  /* ---- SSD1306 初始化序列 ---- */
  OLED_WrCmd(0xAE);        /* 关闭显示 */

  OLED_WrCmd(0x20);        /* 设置内存寻址模式 */
  OLED_WrCmd(0x02);        /* 0x00=水平 0x01=垂直 0x02=页寻址 (本驱动按页寻址写) */

  OLED_WrCmd(0xB0);        /* 页地址 = 0 */
  OLED_WrCmd(0xC8);        /* COM 输出扫描方向: 反向 */
  OLED_WrCmd(0x00);        /* 列地址低 4 位 */
  OLED_WrCmd(0x10);        /* 列地址高 4 位 */
  OLED_WrCmd(0x40);        /* 显示起始行 = 0 */

  OLED_WrCmd(0x81);        /* 对比度 */
  OLED_WrCmd(0xFF);

  OLED_WrCmd(0xA1);        /* 段重映射: 左右翻转 */
  OLED_WrCmd(0xA6);        /* 正常显示 (非反色) */

  OLED_WrCmd(0xA8);        /* 多路复用比 */
  OLED_WrCmd(0x3F);        /* 1/64 duty */

  OLED_WrCmd(0xA4);        /* 输出跟随 RAM 内容 */
  OLED_WrCmd(0xD3);        /* 显示偏移 */
  OLED_WrCmd(0x00);

  OLED_WrCmd(0xD5);        /* 时钟分频 / 振荡频率 */
  OLED_WrCmd(0xF0);

  OLED_WrCmd(0xD9);        /* 预充电周期 */
  OLED_WrCmd(0x22);

  OLED_WrCmd(0xDA);        /* COM 引脚硬件配置 */
  OLED_WrCmd(0x12);        /* 交替模式, 无左右反转 */

  OLED_WrCmd(0xDB);        /* VCOMH 电压倍率 */
  OLED_WrCmd(0x20);

  OLED_WrCmd(0x8D);        /* 电荷泵 */
  OLED_WrCmd(0x14);        /* 开启 */

  OLED_WrCmd(0xAF);        /* 打开显示 */

  OLED_Clear();
}

/* ==========================================================================
 * 清屏
 * ========================================================================== */
void OLED_Clear(void)
{
  for (uint8_t page = 0; page < OLED_PAGES; page++)
  {
    OLED_SetCursor(0, page);
    for (uint8_t col = 0; col < OLED_WIDTH; col++)
    {
      OLED_WrData(0x00);
    }
  }
}

/**
  * @brief  把若干个连续页填成同一个字节图案
  * @param  page_start : 起始页 0~7
  * @param  page_end   : 结束页(含) 0~7
  * @param  pattern    : 0xFF = 全亮, 0x00 = 全灭
  *
  * 调试用: 整屏填充是最容易肉眼判读的测试。
  * 若上半屏白、下半屏黑 = 数据通路与页寻址都正常;
  * 若出现条纹 = 某几根数据线有问题; 若上下颠倒 = 扫描方向参数要改。
  */
void OLED_FillPages(uint8_t page_start, uint8_t page_end, uint8_t pattern)
{
  for (uint8_t page = page_start; page <= page_end && page < OLED_PAGES; page++)
  {
    OLED_SetCursor(0, page);
    for (uint8_t col = 0; col < OLED_WIDTH; col++)
    {
      OLED_WrData(pattern);
    }
  }
}

/**
  * @brief  设置写入起点
  * @param  x    : 列, 0~127
  * @param  page : 页, 0~7 (每页 8 行)
  */
void OLED_SetCursor(uint8_t x, uint8_t page)
{
  OLED_WrCmd((uint8_t)(0xB0 + page));
  OLED_WrCmd((uint8_t)(((x & 0xF0) >> 4) | 0x10));   /* 列高 4 位 */
  OLED_WrCmd((uint8_t)(x & 0x0F));                   /* 列低 4 位 */
}

/* ==========================================================================
 * 显示一个 8x16 字符
 *
 * 字库每个字符 16 字节: 前 8 字节是上半页(0~7 行)的 8 列,
 * 后 8 字节是下半页(8~15 行)的 8 列。页寻址模式下每写一个字节
 * 列地址自动 +1, 所以连续写 8 个字节正好铺满 8 列。
 * ========================================================================== */
void OLED_ShowChar(uint8_t x, uint8_t page, char ch)
{
  if (ch < ' ' || ch > '~')     /* 字库只覆盖可打印 ASCII */
  {
    ch = ' ';
  }

  /* 一个字占两页, 起始页最晚只能是 6 */
  if (x > OLED_WIDTH - OLED_FONT_W || page > OLED_PAGES - 2)
  {
    return;
  }

  const uint8_t *p = oled_asc2_1608[(uint8_t)ch - ' '];

  OLED_SetCursor(x, page);
  for (uint8_t i = 0; i < 8; i++)
  {
    OLED_WrData(p[i]);
  }

  OLED_SetCursor(x, (uint8_t)(page + 1));
  for (uint8_t i = 8; i < 16; i++)
  {
    OLED_WrData(p[i]);
  }
}

/**
  * @brief  显示字符串
  * @param  x    : 起始列 (像素)
  * @param  page : 起始页, 应为偶数 (0 或 2), 因为一个字占两页
  */
void OLED_ShowString(uint8_t x, uint8_t page, const char *str)
{
  while (*str != '\0')
  {
    if (x > OLED_WIDTH - OLED_FONT_W)     /* 一行放不下就换到下一行 */
    {
      x = 0;
      page = (uint8_t)(page + 2);
    }
    if (page > OLED_PAGES - 2)            /* 屏幕写满, 停止 */
    {
      break;
    }

    OLED_ShowChar(x, page, *str);
    x = (uint8_t)(x + OLED_FONT_W);
    str++;
  }
}

/**
  * @brief  显示整数, 高位补空格 (右对齐)
  * @param  len : 总位数
  */
void OLED_ShowNum(uint8_t x, uint8_t page, int32_t num, uint8_t len)
{
  uint32_t pow = 1;
  uint8_t  started = 0;

  for (uint8_t i = 1; i < len; i++)
  {
    pow *= 10;
  }

  for (uint8_t i = 0; i < len; i++)
  {
    uint8_t digit = (uint8_t)(((uint32_t)num / pow) % 10);

    /* 最高位之前的 0 显示成空格; pow==1 时一定显示, 保证 num=0 能显示出 "0" */
    if (digit != 0 || started || pow == 1)
    {
      OLED_ShowChar((uint8_t)(x + i * OLED_FONT_W), page, (char)('0' + digit));
      started = 1;
    }
    else
    {
      OLED_ShowChar((uint8_t)(x + i * OLED_FONT_W), page, ' ');
    }

    pow /= 10;
  }
}

/**
  * @brief  显示整数, 高位补 0 (固定宽度)
  *         适合计数这类需要稳定宽度的场合, 避免数字跳变时闪烁
  */
void OLED_ShowNumZ(uint8_t x, uint8_t page, int32_t num, uint8_t len)
{
  uint32_t pow = 1;

  for (uint8_t i = 1; i < len; i++)
  {
    pow *= 10;
  }

  for (uint8_t i = 0; i < len; i++)
  {
    OLED_ShowChar((uint8_t)(x + i * OLED_FONT_W), page,
                  (char)('0' + (uint8_t)(((uint32_t)num / pow) % 10)));
    pow /= 10;
  }
}
