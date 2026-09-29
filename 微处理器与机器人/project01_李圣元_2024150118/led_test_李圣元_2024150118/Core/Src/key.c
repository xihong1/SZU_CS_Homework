#include "key.h"

static GPIO_TypeDef *const key_port[KEY_NUM] = {GPIOH, GPIOH, GPIOC, GPIOA};
static const uint16_t     key_pin[KEY_NUM]  = {GPIO_PIN_3, GPIO_PIN_2,
                                               GPIO_PIN_13, GPIO_PIN_0};
/* 1 = 按下时为高电平（WK_UP），0 = 按下时为低电平（KEY0~KEY2） */
static const uint8_t      key_active_high[KEY_NUM] = {0, 0, 0, 1};

/**
 * @brief  初始化 4 个按键的 IO（输入模式，带内部上下拉）
 */
void key_init(void)
{
    GPIO_InitTypeDef gpio_init_struct = {0};
    uint8_t i;

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_GPIOH_CLK_ENABLE();

    gpio_init_struct.Mode  = GPIO_MODE_INPUT;
    gpio_init_struct.Speed = GPIO_SPEED_FREQ_LOW;

    for (i = 0; i < KEY_NUM; i++)
    {
        gpio_init_struct.Pin  = key_pin[i];
        /* 低电平有效的按键配内部上拉，高电平有效的配内部下拉 */
        gpio_init_struct.Pull = key_active_high[i] ? GPIO_PULLDOWN : GPIO_PULLUP;
        HAL_GPIO_Init(key_port[i], &gpio_init_struct);
    }
}

/**
 * @brief  判断第 i 个按键当前是否被按下（已统一为 1 = 按下）
 * @retval 1 = 按下，0 = 松开
 */
static uint8_t key_is_pressed(uint8_t i)
{
    GPIO_PinState level = HAL_GPIO_ReadPin(key_port[i], key_pin[i]);

    if (key_active_high[i])
    {
        return (level == GPIO_PIN_SET) ? 1 : 0;      /* WK_UP：高电平表示按下 */
    }

    return (level == GPIO_PIN_RESET) ? 1 : 0;        /* KEY0~2：低电平表示按下 */
}
/**
 * @brief  按键扫描（需要在主循环里反复调用，内部不阻塞）
 * @retval 0 = 没有新的按下事件；1~4 = 第几个按键被按下
 */
uint8_t key_scan(void)
{
    static uint8_t  stable[KEY_NUM];        /* 已确认的稳定状态：1 = 按下 */
    static uint8_t  last_raw[KEY_NUM];      /* 上一次采样的原始状态 */
    static uint32_t change_tick[KEY_NUM];   /* 最近一次电平变化的时间 */
    uint8_t  i;
    uint8_t  raw;
    uint8_t  ret = 0;
    uint32_t now = HAL_GetTick();

    for (i = 0; i < KEY_NUM; i++)
    {
        raw = key_is_pressed(i);

        if (raw != last_raw[i])             /* 电平刚变化：重新开始计时 */
        {
            last_raw[i]    = raw;
            change_tick[i] = now;
        }
        else if ((now - change_tick[i]) >= KEY_DEBOUNCE_MS && raw != stable[i])
        {
            stable[i] = raw;                /* 持续 10ms 没变，认可这个新状态 */

            if (raw != 0)                   /* 只在“按下”的瞬间返回键值 */
            {
                ret = (uint8_t)(i + 1);
            }
        }
        else
        {
            /* 状态没变，什么都不做 */
        }
    }

    return ret;
}
