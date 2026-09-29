# 跑马灯实验源代码（李圣云 2024150118）

本目录是从实验报告 `main.tex` 的代码清单中直接提取出来的源文件，**内容与报告完全一致**，
可以直接覆盖到 STM32CubeIDE 工程里使用。

## 文件清单

| 文件 | 说明 |
| --- | --- |
| `Core/Inc/led.h` | 8 路 LED 的引脚宏定义、4 种特效编号、对外函数声明 |
| `Core/Src/led.c` | 端口数组、`led_init()`、`led_write(mask)`、4 种特效掩码算法、`effect_run()` |
| `Core/Inc/key.h` | 按键数量、消抖时间、对外函数声明 |
| `Core/Src/key.c` | 按键端口表、`key_init()`、`key_is_pressed()`、带消抖的 `key_scan()` |
| `Core/Inc/beep.h` | 蜂鸣器有效电平、鸣响时长、对外函数声明 |
| `Core/Src/beep.c` | 软件 I2C 时序、PCF8574 读写、`beep_init/start/task` |
| `Core/Src/main.c` | 主程序：初始化 + 非阻塞主循环 + 180 MHz 时钟配置 |
| `Core/Inc/main.h` | 8 路 LED 的引脚宏（CubeMX 按 User Label 生成的样子） |
| `Core/Src/gpio.c` / `Core/Inc/gpio.h` | `MX_GPIO_Init()`，配置 PB0、PB3~PB9 为推挽输出 |

## 引脚分配

* **8 路 LED**（都在 GPIOB，低电平点亮，每路串 1 kΩ 到 3.3 V）
  `LED0=PB3  LED1=PB4  LED2=PB5  LED3=PB6  LED4=PB7  LED5=PB8  LED6=PB9  LED7=PB0`
* **4 个按键**：`KEY0=PH3`、`KEY1=PH2`、`KEY2=PC13`（低电平有效）、`KEY3=PA0`（WK_UP，高电平有效）
* **蜂鸣器**：板载，经 PCF8574 的 P0 控制，软件 I2C `SCL=PH4`、`SDA=PH5`，7 位地址 `0x20`
* **系统时钟**：HSE 25 MHz → PLL(M=25, N=360, P=2, Q=4) → SYSCLK 180 MHz

## 使用方法

1. 在 STM32CubeIDE 中用 CubeMX 新建 STM32F429IGT6 工程，按上面的引脚分配配置 GPIO
   （`PB0`、`PB3`~`PB9` 设为 `GPIO_Output`，输出电平 `High`，User Label 依次填 `LED7`、`LED0`~`LED6`），
   时钟树按 180 MHz 配置（详见报告的“实验过程及内容”一节）。
2. 生成代码后，把本目录 `Core/Inc`、`Core/Src` 下的文件复制到工程的对应目录中覆盖。
3. 把 `Core/Src` 里的新文件（`led.c`、`key.c`、`beep.c`）加入工程的编译列表。
4. 编译、下载、复位运行。

## 预期现象

* 上电后默认运行**特效 1 单灯流水**，亮点每 200 ms 右移一格，到 LED7 后回到 LED0 循环。
* 按下 `KEY0`~`KEY3` 分别切换到单灯流水 / 双灯追逐 / 乒乓往返 / 逐个点亮，切换时蜂鸣器响一声约 80 ms。
* 按住按键不放，蜂鸣器**不会**连续鸣响，灯效**不会**反复切换。

## 如果编译或运行不正常

* **LED 全不亮**：先量 GPIO 引脚电平确认程序有没有在跑；若电平在变，检查 LED 长短脚是否接反。
* **灯的最亮位置与预期相反**：把 `led_init()` 与 `led_write()` 里的 `GPIO_PIN_SET` / `GPIO_PIN_RESET` 对调。
* **蜂鸣器一直响或按键时不响**：把 `beep.h` 里的 `BEEP_ON_LEVEL` 在 `0` 和 `1` 之间改一下即可。
* **程序卡死、LED 全灭**：多半是 HSE 没起振。先临时把 `SystemClock_Config()` 换回内部 HSI 排查，
  确认是时钟源问题后再核对晶振频率与 PLLM/PLLN/PLLP 的取值。
