#ifndef __BEEP_H
#define __BEEP_H

#include "main.h"

/* 板载蜂鸣器接在 PCF8574 的 P0 脚上，通过 I2C 控制
 *   板上的 I2C 总线（与 24C02 共用）：PH4 = SCL，PH5 = SDA
 *   PCF8574 地址线 A0~A2 全部接地，7 位地址 0x20（写地址 0x40）
 */

/* P0 输出 0 = 蜂鸣器响。若实测相反，改成 1 即可 */
#define BEEP_ON_LEVEL       0

#define BEEP_DEFAULT_MS     80      /* 按键提示音时长：80ms */

void beep_init(void);
void beep_start(uint16_t ms);       /* 让蜂鸣器开始响，ms 毫秒后自动关闭 */
void beep_task(void);               /* 需要在主循环里反复调用 */

#endif /* __BEEP_H */
