#include "led.h"

/* 8 个 LED 的端口与引脚，下标 i 对应 LEDi */
static GPIO_TypeDef *const led_port[LED_NUM] = {
    LED0_PORT, LED1_PORT, LED2_PORT, LED3_PORT,
    LED4_PORT, LED5_PORT, LED6_PORT, LED7_PORT
};

static const uint16_t led_pin[LED_NUM] = {
    LED0_PIN, LED1_PIN, LED2_PIN, LED3_PIN,
    LED4_PIN, LED5_PIN, LED6_PIN, LED7_PIN
};

/**
 * @brief  初始化 8 个 LED 的 IO 口（推挽输出，上电默认熄灭）
 */
void led_init(void)
{
    GPIO_InitTypeDef gpio_init_struct = {0};
    uint8_t i;

    __HAL_RCC_GPIOB_CLK_ENABLE();                    /* 8 个 LED 都在 GPIOB 上 */

    gpio_init_struct.Mode  = GPIO_MODE_OUTPUT_PP;    /* 推挽输出 */
    gpio_init_struct.Pull  = GPIO_PULLUP;            /* 上拉 */
    gpio_init_struct.Speed = GPIO_SPEED_FREQ_LOW;    /* 驱动 LED 用低速就够 */

    for (i = 0; i < LED_NUM; i++)
    {
        gpio_init_struct.Pin = led_pin[i];
        HAL_GPIO_Init(led_port[i], &gpio_init_struct);
        HAL_GPIO_WritePin(led_port[i], led_pin[i], GPIO_PIN_SET);  /* 高电平 = 灯灭 */
    }
}

/**
 * @brief  按掩码刷新 8 个 LED
 * @param  mask: bit0~bit7 依次对应 LED0~LED7，某位为 1 表示该灯点亮
 */
void led_write(uint8_t mask)
{
    uint8_t i;

    for (i = 0; i < LED_NUM; i++)
    {
        /* 低电平点亮：掩码位为 1 输出低电平，为 0 输出高电平 */
        if (mask & (1 << i))
        {
            HAL_GPIO_WritePin(led_port[i], led_pin[i], GPIO_PIN_RESET);
        }
        else
        {
            HAL_GPIO_WritePin(led_port[i], led_pin[i], GPIO_PIN_SET);
        }
    }
}
/* --------------------- 4 种特效的掩码算法 --------------------- */

/**
 * @brief  特效1：单灯流水 —— 只有一个灯亮，位置依次右移
 */
static uint8_t effect_flow_mask(uint16_t step)
{
    return (uint8_t)(1 << (step % LED_NUM));
}

/**
 * @brief  特效2：双灯追逐 —— 两个亮点相隔 4 个位置同时移动
 */
static uint8_t effect_double_mask(uint16_t step)
{
    uint8_t a = (uint8_t)(step % LED_NUM);
    uint8_t b = (uint8_t)((a + LED_NUM / 2) % LED_NUM);

    return (uint8_t)((1 << a) | (1 << b));
}

/**
 * @brief  特效3：乒乓往返 —— 亮点先从头走到尾，再从尾走回头（两端不重复）
 */
static uint8_t effect_bounce_mask(uint16_t step)
{
    uint16_t period = (uint16_t)(2 * LED_NUM - 2);   /* 14 个位置循环 */
    uint16_t pos    = (uint16_t)(step % period);

    if (pos >= LED_NUM)
    {
        pos = (uint16_t)(period - pos);              /* 利用对称性折返 */
    }

    return (uint8_t)(1 << pos);
}

/**
 * @brief  特效4：逐个点亮 —— 亮的灯数从 0 个逐个增加到 8 个，然后重新开始
 */
static uint8_t effect_fill_mask(uint16_t step)
{
    uint16_t num = (uint16_t)(step % (LED_NUM + 1));
    uint8_t  mask = 0;
    uint8_t  i;

    for (i = 0; i < num; i++)
    {
        mask |= (uint8_t)(1 << i);                   /* 低 num 位全置 1 */
    }

    return mask;
}
/**
 * @brief  执行第 effect 种特效的第 step 步
 * @param  effect: 特效编号（EFFECT_FLOW / EFFECT_DOUBLE / ...）
 * @param  step  : 步数，从 0 开始递增
 */
void effect_run(uint8_t effect, uint16_t step)
{
    uint8_t mask = 0;

    switch (effect)
    {
        case EFFECT_FLOW:   mask = effect_flow_mask(step);   break;
        case EFFECT_DOUBLE: mask = effect_double_mask(step); break;
        case EFFECT_BOUNCE: mask = effect_bounce_mask(step); break;
        case EFFECT_FILL:   mask = effect_fill_mask(step);   break;
        default:            mask = 0;                        break;
    }

    led_write(mask);        /* 算出来的掩码立刻刷新到 8 个引脚上 */
}

/**
 * @brief  取某种特效每一步的间隔时间（ms）
 */
uint16_t effect_interval(uint8_t effect)
{
    switch (effect)
    {
        case EFFECT_FLOW:   return 200;   /* 流水：慢一点更清楚 */
        case EFFECT_DOUBLE: return 200;
        case EFFECT_BOUNCE: return 150;   /* 往返：稍快 */
        case EFFECT_FILL:   return 120;   /* 逐个点亮：最快 */
        default:            return 200;
    }
}
