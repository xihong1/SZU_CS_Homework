/**
  ******************************************************************************
  * @file    led.c
  * @brief   板载 LED 驱动
  *
  * 阿波罗开发板 LED 电路为: 3.3V -> 限流电阻 -> LED -> GPIO,
  * 所以 GPIO 输出低电平时灯亮, 是"低电平点亮"。
  ******************************************************************************
  */

#include "led.h"
#include "app_config.h"

static GPIO_TypeDef *const led_port[2] = { LED0_GPIO_PORT, LED1_GPIO_PORT };
static const uint16_t      led_pin [2] = { LED0_GPIO_PIN,  LED1_GPIO_PIN  };

void led_init(void)
{
  GPIO_InitTypeDef gpio = {0};

  __HAL_RCC_GPIOB_CLK_ENABLE();

  /* 先输出高电平, 保证配置完成前灯是灭的 */
  HAL_GPIO_WritePin(LED0_GPIO_PORT, LED0_GPIO_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(LED1_GPIO_PORT, LED1_GPIO_PIN, GPIO_PIN_SET);

  gpio.Mode  = GPIO_MODE_OUTPUT_PP;
  gpio.Pull  = GPIO_NOPULL;
  gpio.Speed = GPIO_SPEED_FREQ_LOW;

  gpio.Pin = LED0_GPIO_PIN;
  HAL_GPIO_Init(LED0_GPIO_PORT, &gpio);

  gpio.Pin = LED1_GPIO_PIN;
  HAL_GPIO_Init(LED1_GPIO_PORT, &gpio);
}

void led_on(uint8_t idx)
{
  if (idx < 2)
  {
    led_port[idx]->BSRR = (uint32_t)led_pin[idx] << 16;   /* 置低 -> 点亮 */
  }
}

void led_off(uint8_t idx)
{
  if (idx < 2)
  {
    led_port[idx]->BSRR = led_pin[idx];                  /* 置高 -> 熄灭 */
  }
}

void led_toggle(uint8_t idx)
{
  if (idx < 2)
  {
    led_port[idx]->ODR ^= led_pin[idx];
  }
}
