/**
 ******************************************************************************
 * @file    beep.c
 * @brief   板载蜂鸣器控制（通过软件 I2C 控制 PCF8574 的 P0 脚）
 *
 *  程序结构：
 *    1) 底层：软件模拟 I2C 时序（start / send_byte / stop）
 *    2) 中层：PCF8574 的写字节、写单个位
 *    3) 上层：beep_init / beep_start / beep_task —— 只对外提供这三个接口
 *
 *  为什么响 80ms 不用 HAL_Delay？
 *    用 HAL_Delay(80) 会让 CPU 空等，期间按键扫描和灯效更新全部停住，
 *    表现就是“按键反应迟钝、灯效卡顿”。这里改用时间戳判断，
 *    主循环照常运行，到时间自动关掉蜂鸣器。
 ******************************************************************************
 */
#include "beep.h"

/* ==================== 一、软件 I2C 底层 ==================== */
#define IIC_SCL_PORT        GPIOH
#define IIC_SCL_PIN         GPIO_PIN_4
#define IIC_SDA_PORT        GPIOH
#define IIC_SDA_PIN         GPIO_PIN_5

#define PCF8574_ADDR_W      0x40    /* 7 位地址 0x20 左移一位 + 写方向 0 */

/**
 * @brief  I2C 位延时（约 1~2us，I2C 对速度要求不严格，慢一点更稳）
 */
static void iic_delay(void)
{
    volatile uint16_t i;
    for (i = 0; i < 8; i++)
    {
        __NOP();
    }
}

static void iic_scl(uint8_t level)
{
    HAL_GPIO_WritePin(IIC_SCL_PORT, IIC_SCL_PIN, level ? GPIO_PIN_SET : GPIO_PIN_RESET);
    iic_delay();
}

static void iic_sda(uint8_t level)
{
    HAL_GPIO_WritePin(IIC_SDA_PORT, IIC_SDA_PIN, level ? GPIO_PIN_SET : GPIO_PIN_RESET);
    iic_delay();
}

static uint8_t iic_sda_read(void)
{
    return (HAL_GPIO_ReadPin(IIC_SDA_PORT, IIC_SDA_PIN) == GPIO_PIN_SET) ? 1 : 0;
}

/* 产生起始信号：SCL 为高时，SDA 由高变低 */
static void iic_start(void)
{
    iic_sda(1);
    iic_scl(1);
    iic_sda(0);
    iic_scl(0);
}

/* 产生停止信号：SCL 为高时，SDA 由低变高 */
static void iic_stop(void)
{
    iic_sda(0);
    iic_scl(1);
    iic_sda(1);
    iic_delay();
}

/**
 * @brief  发送一个字节
 * @retval 0 = 从机应答（ACK），1 = 无应答（NACK）
 */
static uint8_t iic_send_byte(uint8_t txd)
{
    uint8_t t;
    uint8_t ack;

    for (t = 0; t < 8; t++)
    {
        iic_sda((txd & 0x80) ? 1 : 0);      /* 先发最高位 */
        txd <<= 1;
        iic_scl(1);
        iic_scl(0);
    }

    iic_sda(1);                             /* 释放 SDA，等从机应答 */
    iic_scl(1);
    ack = iic_sda_read();                   /* 0 = 有应答 */
    iic_scl(0);

    return ack;
}

/* ==================== 二、PCF8574 操作 ==================== */

/**
 * @brief  向 PCF8574 写一个字节，会同时刷新 P0~P7 的输出
 */
static void pcf8574_write_byte(uint8_t data)
{
    iic_start();
    iic_send_byte(PCF8574_ADDR_W);
    iic_send_byte(data);
    iic_stop();
}

/**
 * @brief  控制 PCF8574 的某一位（bit: 0~7，sta: 0 或 1）
 */
static void pcf8574_write_bit(uint8_t bit, uint8_t sta)
{
    static uint8_t out_buf = 0xFF;          /* 输出锁存：默认全部输出高电平 */

    if (sta)
    {
        out_buf |= (uint8_t)(1 << bit);
    }
    else
    {
        out_buf &= (uint8_t)~(1 << bit);
    }

    pcf8574_write_byte(out_buf);
}

/* ==================== 三、对外接口 ==================== */

static uint32_t beep_off_tick = 0;          /* 该关掉蜂鸣器的时间点 */
static uint8_t  beeping       = 0;          /* 1 = 正在响 */

/**
 * @brief  初始化：把 PH4/PH5 配成开漏输出，并把 PCF8574 所有输出置为"不响"
 */
void beep_init(void)
{
    GPIO_InitTypeDef gpio_init_struct = {0};

    __HAL_RCC_GPIOH_CLK_ENABLE();

    gpio_init_struct.Pin   = IIC_SCL_PIN | IIC_SDA_PIN;
    gpio_init_struct.Mode  = GPIO_MODE_OUTPUT_OD;   /* I2C 必须是开漏输出 */
    gpio_init_struct.Pull  = GPIO_PULLUP;           /* 配合内部上拉，空闲时为高 */
    gpio_init_struct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    HAL_GPIO_Init(GPIOH, &gpio_init_struct);

    iic_scl(1);
    iic_sda(1);

    pcf8574_write_byte(0xFF);                       /* 全部输出高电平 = 蜂鸣器不响 */
}

/**
 * @brief  让蜂鸣器响 ms 毫秒（不阻塞主循环）
 */
void beep_start(uint16_t ms)
{
    pcf8574_write_bit(0, BEEP_ON_LEVEL);            /* P0 = 响 */
    beep_off_tick = HAL_GetTick() + ms;
    beeping       = 1;
}

/**
 * @brief  蜂鸣器计时处理（主循环里调用）
 */
void beep_task(void)
{
    if (beeping && ((int32_t)(HAL_GetTick() - beep_off_tick) >= 0))
    {
        pcf8574_write_bit(0, (uint8_t)!BEEP_ON_LEVEL);  /* P0 = 不响 */
        beeping = 0;
    }
}
