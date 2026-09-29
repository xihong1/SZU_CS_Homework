# STM32F429 跑马灯实验 · 进度记录

> 本文件由 AI 助手在 2026-09-21 整理，用于在重启电脑、重开会话后快速恢复上下文。
> 配套文件（都在桌面）：`flash_and_run.bat`、`cmsis-dap-swd.cfg`

---

## 一、关键路径（重启后照着找）

| 项目 | 路径 |
| --- | --- |
| CubeIDE 程序 | `C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\stm32cubeide.exe` |
| 工作区 | `C:\Users\23609\Desktop\workspaceSTM32` |
| 工程目录 | `C:\Users\23609\Desktop\workspaceSTM32\led_test` |
| F4 固件包 | `C:\Users\23609\STM32Cube\Repository\STM32Cube_FW_F4_V1.27.1` |
| DAP 调试配置 | 工程根目录 `cmsis-dap-swd.cfg`（桌面有副本） |
| 一键烧录工具 | 桌面 `flash_and_run.bat` |
| 原 180MHz 时钟备份 | `led_test\main.c.180MHz备份` |
| 老师给的资料 | `C:\Users\23609\Desktop\微电子` |
| 实验报告模板 | `C:\Users\23609\Desktop\project1`（LaTeX 模板） |

OpenOCD 与脚本目录（`flash_and_run.bat` 里已写好，一般不用手敲）：

```
OpenOCD:  C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.openocd.win32_2.3.0.202305091550\tools\bin\openocd.exe
脚本目录: C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.debug.openocd_2.1.0.202306221132\resources\openocd\st_scripts
```

---

## 二、已解决的问题（含原因，报告里可以写）

### 1. 要不要装 Java？—— 不用
CubeIDE 1.13.1 **自带** Adoptium Temurin 17 JRE（官方发行说明 DM00603738 里写明）。
老师教程里"先装 Java 8"是给老版本写的，可以跳过。

### 2. DAP 仿真器怎么让 CubeIDE 认得
CubeIDE 原生只支持 ST-LINK，用 DAP 必须改 OpenOCD 脚本，两处修改：

```
source [find interface/stlink-dap.cfg]   →   source [find interface/cmsis-dap.cfg]
transport select "dapdirect_swd"         →   transport select "swd"
```

**另外必须去掉 `connect_assert_srst`**（即 `set CONNECT_UNDER_RESET 0`）。
加上它以后，正点原子 DAP 会把目标复位线一直拉低，导致反复报
`Cortex-M PARTNO 0x0 is unrecognized` 而无法连接。这是踩过的大坑之一。

改好的文件：`led_test\cmsis-dap-swd.cfg`，并在 CubeIDE 里
`Run → Debug Configurations → Debugger → Configuration Script` 选到它（User Defined）。

### 3. 【重要】BOOT0 问题：复位后芯片跑进 Bootloader
两块开发板现象完全一致：**上电/按复位后，PC 停在 `0x1FFFxxxx`（出厂 Bootloader）**，
而不是运行 Flash 里的程序。原因是实验箱底板把 BOOT0 拉高了（核心板上 BOOT0 只有 100K 下拉，
没有跳线）。

**临时解决办法**：烧录后手动把 CPU 跳到程序入口（`flash_and_run.bat` 已包含这一步）：

```
program <elf> verify
mww 0xE000ED08 0x08000000      ← 设置向量表在 Flash
set sp [mrw 0x08000000]        ← 从 Flash 第一个字取栈顶
set rp [mrw 0x08000004]        ← 从 Flash 第二个字取程序入口
reg msp $sp ; reg pc $rp ; resume
```

**彻底解决**：需要问老师/助教"这块实验箱底板的 BOOT0 怎么置低"，或找到底板上的相关跳线/开关。

### 4. 【重要】180 MHz 时钟跑不起来
用 HSE 25MHz + PLL 配到 180 MHz（含 Over-drive、5 个 Flash 等待周期）时，
程序一跑就崩（故障寄存器记录"取到非法指令"，属于双重故障）。
**改成内部 HSI 16 MHz 后一切正常**。
跑马灯、按键、蜂鸣器、PWM 呼吸灯都不需要高主频，16 MHz 完全够用。
（怀疑是底板供电/晶振质量或芯片体质问题，需要时可再排查：试试 120 MHz。）

### 5. 板载蜂鸣器不在 MCU 引脚上
阿波罗 F429 的板载蜂鸣器接在 **PCF8574**（I2C 扩展芯片）的 **P0** 脚上：

| 项目 | 值 |
| --- | --- |
| I2C 引脚 | PH4 = SCL，PH5 = SDA（与 24C02 共用总线） |
| PCF8574 地址 | 7 位 `0x20`（A0~A2 接地），写地址 `0x40` |
| 蜂鸣器 | P0，写 0 = 响（极性若相反，改 `beep.h` 里 `BEEP_ON_LEVEL`） |
| 驱动方式 | 代码里用**软件模拟 I2C**（不占用硬件 I2C 外设） |

---

## 三、当前工程状态

### 引脚分配

| 用途 | 引脚 | 说明 |
| --- | --- | --- |
| LED1 | PB1 | 板载 DS0 红灯 |
| LED2 | PB0 | 板载 DS1 绿灯 |
| LED3~LED8 | PB3、PB4、PB5、PB6、PB7、PB9 | 面包板上的 6 个 LED（PB10 曾用过，后改成 PB9） |
| KEY0~KEY3 | PH3、PH2、PC13、PA0 | 板载 4 个按键（PA0 是 WK_UP） |
| 蜂鸣器 | PCF8574 的 P0（PH4/PH5） | 板载 |

接线方式（每个外接 LED）：`3.3V ──[1K 电阻]── LED 长脚 ── LED 短脚 ── 对应引脚`，IO 输出低电平点亮。

### 源文件

| 文件 | 内容 |
| --- | --- |
| `Core/Src/led.c` / `Core/Inc/led.h` | 8 路 LED 驱动 + 4 种灯效算法（引脚宏定义集中在这里） |
| `Core/Src/key.c` / `Core/Inc/key.h` | 4 个按键扫描、10ms 消抖、"按下事件"检测 |
| `Core/Src/beep.c` / `Core/Inc/beep.h` | 软件 I2C + PCF8574 + 蜂鸣器（非阻塞计时） |
| `Core/Src/main.c` | 主循环：读按键 → 切换灯效 + 蜂鸣器响一声；按时间戳推进灯效 |

### 4 种灯效与按键对应

| 按键 | 灯效 | 算法 | 步进间隔 |
| --- | --- | --- | --- |
| KEY0 (PH3) | 单灯流水 | 第 step 个灯亮 | 200ms |
| KEY1 (PH2) | 双灯追逐 | 相隔 4 位的两个灯亮 | 200ms |
| KEY2 (PC13) | 乒乓往返 | 亮点 0→7 再 7→0 | 150ms |
| WK_UP (PA0) | 逐个点亮 | 亮的灯数 0→8 递增 | 120ms |

设计要点（报告可写）：灯效不用 `HAL_Delay` 阻塞，而是用时间戳判断推进，
所以按键随时都能响应；按键消抖用"电平变化后保持 10ms 才认可"的办法，
且只在"按下瞬间"返回键值，保证一次按键只响一声。

---

## 四、日常怎么继续干活

**改代码 → 编译 → 烧录：**

1. 在 CubeIDE 里改代码，按 `Ctrl+B` 编译
2. 双击桌面 `flash_and_run.bat`（会烧录并自动把程序跑起来）
3. 注意：**烧录前 CubeIDE 里不能有调试会话开着**，否则仿真器被占用

**改引脚**：只改 `Core/Inc/led.h` 里的 `LEDx_PORT / LEDx_PIN` 宏定义，逻辑代码不用动。

**改蜂鸣器极性**：改 `Core/Inc/beep.h` 里的 `BEEP_ON_LEVEL`（0 或 1）。

**命令行编译**（bat 之外的方式，一般用不到）：

```
PATH 里加上：
C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-tools-for-stm32.11.3.rel1.win32_1.1.0.202305231506\tools\bin
C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.make.win32_2.1.0.202305091550\tools\bin
然后在 led_test\Debug 目录下执行 make all
```

---

## 五、故障排查速查表

| CubeIDE / OpenOCD 报错 | 含义 | 处理 |
| --- | --- | --- |
| `Error connecting DP: cannot read IDR` | 芯片完全没回应（硬件侧） | 检查开发板电源灯、20P 排线两头插紧、重插 |
| `Cortex-M PARTNO 0x0 is unrecognized` | 复位线被拉住 / 连接模式不对 | 拔插 DAP 的 USB 线重置它；确认 cfg 里没有 `connect_assert_srst` |
| `CMSIS-DAP command mismatch` | 仿真器被别的进程占用 | 关掉 CubeIDE 的调试会话（红色方块） |
| 烧录成功但灯不闪 | 芯片跑进 Bootloader | 用 `flash_and_run.bat`（含手动跳转）；或问老师 BOOT0 |
| 按复位后灯不闪 | 同上 | 同上（这是底板电路导致的，不是板子坏） |

---

## 六、待办事项

- [ ] 验证**板载蜂鸣器**：按 4 个按键任意一个应"嘀"一声；若现象相反，改 `BEEP_ON_LEVEL`
- [ ] 验证 4 个按键能正常切换灯效
- [ ] 选做：**PWM 呼吸灯**（可用空闲的 TIM2/3/4 输出 PWM，注意 `HAL_TIM_MODULE_ENABLED` 已在 hal_conf.h 中打开）
- [ ] 问老师/助教：**实验箱底板的 BOOT0 怎么置低**（让程序能自己跑起来，不用每次手动跳转）
- [ ] 写**实验报告**（模板在桌面 `project1`，报告要求见模板里"一、实验目的与要求"）
- [ ] 报告里如实说明：主频采用 16 MHz（180 MHz 在本实验箱上不稳定）

---

## 七、给以后的自己/助手的一句话背景

> 深圳大学《微处理器与机器人》跑马灯实验：用 STM32F429IGT6（阿波罗 V2 核心板 + DNF429-EB 实验箱）
> 和 STM32CubeIDE 1.13.1 实现 8 个 LED、4 种灯效、4 个按键切换、按键蜂鸣器提示音。
> 板子通过 DAP（CMSIS-DAP）经 OpenOCD 下载调试；因实验箱底板把 BOOT0 拉高，
> 每次上电/复位后需用 OpenOCD 手动把 PC 指向 Flash 入口来启动程序。
