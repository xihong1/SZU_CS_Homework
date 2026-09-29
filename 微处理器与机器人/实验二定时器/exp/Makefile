##############################################################################
# STM32F429IGT6 (正点原子阿波罗开发板) 定时器实验
#
# 注意(踩过的坑): 必须显式指定默认目标。
#   GNU Make 会把"第一条出现的规则"当成默认目标。编译器的 .d 依赖文件里
#   全是 `build/xxx.o: ...` 这样的规则, 如果把它们 -include 在 all: 之前,
#   第一个 .o 就会变成默认目标 —— make 编完那一个文件就收工, 看起来"编译成功"
#   其实什么都没更新, 烧进去的还是旧程序。所以这里显式设置 .DEFAULT_GOAL,
#   并把 -include 放到文件末尾。
#
# 工具链: Arm GNU Toolchain (arm-none-eabi-gcc) + mingw32-make + pyOCD
# 用法:
#   make            编译, 生成 build/firmware.elf/.hex/.bin
#   make flash      用 pyOCD 烧录
#   make verify     回读 FLASH 校验
#   make reset      复位并运行
#   make clean      清理
#
# 若 arm-none-eabi-gcc 不在 PATH 中, 先执行:
#   source tools/toolchain_env.sh
##############################################################################

TARGET   := firmware
BUILD    := build

# 显式指定默认目标, 避免被 -include 进来的 .d 文件里的规则抢走 (见文件头说明)
.DEFAULT_GOAL := all

# ---- 源文件目录 ----
CORE_SRC := Core/Src
STARTUP  := deps/cmsis_device_f4/Source/Templates/gcc/startup_stm32f429xx.s
CMSIS_SYS:= deps/cmsis_device_f4/Source/Templates/system_stm32f4xx.c

# ---- 包含路径 ----
C_INCLUDES := \
  -ICore/Inc \
  -IBSP/Inc \
  -IApp/Inc \
  -Ideps/stm32f4xx_hal_driver/Inc \
  -Ideps/cmsis_device_f4/Include \
  -Ideps/cmsis_core/CMSIS/Core/Include

# ---- 预处理宏 ----
C_DEFS := -DUSE_HAL_DRIVER -DSTM32F429xx

# ---- 编译选项 ----
MCU      := -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard
OPT      ?= -Og
# -MMD -MP 让编译器为每个 .o 生成一份 .d 依赖文件, 里面记录了它用到的所有头文件。
# 没有这个, 改头文件(比如重新生成字库 oledfont.h)不会触发 .c 重编,
# 烧进去的就是旧代码 —— 这种"改了没生效"的问题极难排查。
C_FLAGS  := $(MCU) $(C_DEFS) $(C_INCLUDES) $(OPT) -g3 -Wall -Wextra \
            -ffunction-sections -fdata-sections -std=gnu11 -MMD -MP
AS_FLAGS := $(MCU) $(OPT) -g3 -Wall -x assembler-with-cpp

# ---- 链接选项 ----
LDSCRIPT := ld/STM32F429IGTx_FLASH.ld
LD_FLAGS := $(MCU) -T$(LDSCRIPT) --specs=nano.specs --specs=nosys.specs \
            -Wl,-Map=$(BUILD)/$(TARGET).map,--cref \
            -Wl,--gc-sections -Wl,--print-memory-usage

# ---- 工具 ----
CC      := arm-none-eabi-gcc
AS      := arm-none-eabi-gcc -x assembler-with-cpp
OBJCOPY := arm-none-eabi-objcopy
SIZE    := arm-none-eabi-size
GDB     := arm-none-eabi-gdb
PYOCD   := python -m pyocd
TARGET_MCU := stm32f429xi

# ---- 需要编译的 HAL 模块 (只取用到的, 加快编译) ----
HAL_SRC := \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_cortex.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_dma.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_dma_ex.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_exti.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_flash.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_flash_ex.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_gpio.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_pwr.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_pwr_ex.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_rcc.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_rcc_ex.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_tim.c \
  deps/stm32f4xx_hal_driver/Src/stm32f4xx_hal_tim_ex.c

# ---- 应用源码 (BSP + 各实验任务) ----
APP_SRC := $(wildcard $(CORE_SRC)/*.c) \
           $(wildcard BSP/Src/*.c) \
           $(wildcard App/Src/*.c)

# ---- 汇总 ----
C_SOURCES := $(APP_SRC) $(HAL_SRC) $(CMSIS_SYS)
OBJECTS   := $(addprefix $(BUILD)/,$(notdir $(C_SOURCES:.c=.o)))
vpath %.c $(sort $(dir $(C_SOURCES)))
OBJECTS   += $(addprefix $(BUILD)/,$(notdir $(STARTUP:.s=.o)))
vpath %.s $(sort $(dir $(STARTUP)))

# ============================================================================
# 目标
# ============================================================================
.PHONY: all clean flash verify reset size elf hex bin

all: $(BUILD)/$(TARGET).elf $(BUILD)/$(TARGET).hex $(BUILD)/$(TARGET).bin

$(BUILD)/%.o: %.c Makefile | $(BUILD)
	@echo "  CC      $<"
	@$(CC) -c $(C_FLAGS) $< -o $@

$(BUILD)/%.o: %.s Makefile | $(BUILD)
	@echo "  AS      $<"
	@$(CC) -c $(AS_FLAGS) $< -o $@

$(BUILD)/$(TARGET).elf: $(OBJECTS) Makefile $(LDSCRIPT)
	@echo "  LD      $@"
	@$(CC) $(OBJECTS) $(LD_FLAGS) -o $@
	@$(SIZE) $@

$(BUILD)/%.hex: $(BUILD)/%.elf
	@echo "  OBJCOPY $@"
	@$(OBJCOPY) -O ihex $< $@

$(BUILD)/%.bin: $(BUILD)/%.elf
	@echo "  OBJCOPY $@"
	@$(OBJCOPY) -O binary -S $< $@

$(BUILD):
	@mkdir -p $@

# ---- 烧录与验证 ----
flash: $(BUILD)/$(TARGET).elf
	@echo "  FLASH   $(TARGET).elf  ->  $(TARGET_MCU)"
	@$(PYOCD) flash -t $(TARGET_MCU) --format elf $<

verify: $(BUILD)/$(TARGET).hex
	@echo "  VERIFY  $(TARGET).hex"
	@$(PYOCD) flash -t $(TARGET_MCU) --format hex --verify-only $<

reset:
	@echo "  RESET   target"
	@$(PYOCD) reset -t $(TARGET_MCU)

size: $(BUILD)/$(TARGET).elf
	@$(SIZE) -A -x $<

clean:
	@echo "  CLEAN"
	@rm -rf $(BUILD)

# ============================================================================
# 头文件依赖: 由 -MMD -MP 在编译时自动生成, 必须放在文件末尾,
# 否则里面的 `build/xxx.o: ...` 规则会变成默认目标 (见文件头说明)。
# -include 遇到不存在的 .d 文件不会报错, 首次编译时正好用得上。
# ============================================================================
-include $(OBJECTS:.o=.d)
