/**
  ******************************************************************************
  * @file    key.c
  * @brief   板载按键驱动, 软件消抖
  ******************************************************************************
  */

#include "key.h"
#include "app_config.h"

/* 连续读到多少次相反电平才认可状态真的变了。
 * key_poll() 每 1 ms 调一次, 所以 10 次 = 10 ms 消抖窗口。 */
#define KEY_DEBOUNCE_TICKS   10

typedef struct
{
  GPIO_TypeDef *port;
  uint16_t      pin;
  uint8_t       active_high;   /* 1 = 按下时为高电平 (WK_UP) */
  uint8_t       stable;        /* 消抖后的稳定状态, 1 = 按下 */
  uint8_t       cnt;           /* 与稳定状态连续不同的采样次数 */
  uint8_t       event;         /* "按下"边沿事件, 取走后清零 */
} key_t;

static key_t s_keys[KEY_COUNT] =
{
  { KEY0_GPIO_PORT, KEY0_GPIO_PIN, 0, 0, 0, 0 },
  { KEY1_GPIO_PORT, KEY1_GPIO_PIN, 0, 0, 0, 0 },
  { KEY2_GPIO_PORT, KEY2_GPIO_PIN, 0, 0, 0, 0 },
  { WKUP_GPIO_PORT, WKUP_GPIO_PIN, 1, 0, 0, 0 },
};

void key_init(void)
{
  GPIO_InitTypeDef gpio = {0};

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();

  gpio.Mode  = GPIO_MODE_INPUT;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;

  /* KEY0/KEY1/KEY2 按下接地, 所以内部上拉 */
  gpio.Pull = GPIO_PULLUP;
  gpio.Pin = KEY0_GPIO_PIN;
  HAL_GPIO_Init(KEY0_GPIO_PORT, &gpio);
  gpio.Pin = KEY1_GPIO_PIN;
  HAL_GPIO_Init(KEY1_GPIO_PORT, &gpio);
  gpio.Pin = KEY2_GPIO_PIN;
  HAL_GPIO_Init(KEY2_GPIO_PORT, &gpio);

  /* WK_UP 按下接 VCC, 所以内部下拉 */
  gpio.Pull = GPIO_PULLDOWN;
  gpio.Pin = WKUP_GPIO_PIN;
  HAL_GPIO_Init(WKUP_GPIO_PORT, &gpio);

  /* 上电时先采一次实际电平作为初始稳定态, 避免刚启动就误报按下 */
  for (int i = 0; i < KEY_COUNT; i++)
  {
    key_t *k = &s_keys[i];
    uint8_t raw = (HAL_GPIO_ReadPin(k->port, k->pin) == GPIO_PIN_SET) ? 1 : 0;
    k->stable = k->active_high ? raw : (uint8_t)!raw;
    k->cnt    = 0;
    k->event  = 0;
  }
}

/**
  * @brief  按 1 ms 节拍轮询所有按键
  *
  * 消抖思路: 只有当"新电平"连续出现 KEY_DEBOUNCE_TICKS 次, 才认可状态翻转。
  * 中途只要抖回原状态, 计数就清零, 所以短于 10 ms 的抖动不会产生事件。
  */
void key_poll(void)
{
  for (int i = 0; i < KEY_COUNT; i++)
  {
    key_t  *k = &s_keys[i];
    uint8_t raw = (HAL_GPIO_ReadPin(k->port, k->pin) == GPIO_PIN_SET) ? 1 : 0;

    if (!k->active_high)
    {
      raw = (uint8_t)!raw;          /* 低电平有效 -> 取反成"是否按下" */
    }

    if (raw == k->stable)
    {
      k->cnt = 0;
    }
    else if (++k->cnt >= KEY_DEBOUNCE_TICKS)
    {
      k->stable = raw;
      k->cnt    = 0;
      if (raw)
      {
        k->event = 1;               /* 只在"按下"的边沿产生事件 */
      }
    }
  }
}

uint8_t key_is_down(key_id_t k)
{
  return (k < KEY_COUNT) ? s_keys[k].stable : 0;
}

uint8_t key_take_press(key_id_t k)
{
  if (k >= KEY_COUNT || s_keys[k].event == 0)
  {
    return 0;
  }
  s_keys[k].event = 0;              /* 取走即清零, 按着不放也只算一次 */
  return 1;
}
