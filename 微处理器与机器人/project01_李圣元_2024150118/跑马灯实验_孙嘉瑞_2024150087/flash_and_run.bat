@echo off
chcp 65001 >nul
title Flash and Run

set "OCD=C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.openocd.win32_2.3.0.202305091550\tools\bin\openocd.exe"
set "SCRIPTS=C:\ST\STM32CubeIDE_1.13.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.debug.openocd_2.1.0.202306221132\resources\openocd\st_scripts"
set "CFG=C:\Users\23609\Desktop\workspaceSTM32\led_test\cmsis-dap-swd.cfg"
set "ELF=C:/Users/23609/Desktop/workspaceSTM32/led_test/Debug/led_test.elf"

if not exist "%OCD%" echo [ERROR] openocd not found & pause & exit /b 1
if not exist "%ELF%" echo [ERROR] elf not found, please build in CubeIDE first & pause & exit /b 1

tasklist /FI "IMAGENAME eq openocd.exe" 2>nul | find /I "openocd.exe" >nul
if not errorlevel 1 echo [INFO] CubeIDE debug session is running. Stop it first. & pause & exit /b 1

echo Flashing and starting program ...
"%OCD%" -s "%SCRIPTS%" -f "%CFG%" -c "init" -c "halt" -c "program {%ELF%} verify" -c "mww 0xE000ED08 0x08000000" -c "set sp [mrw 0x08000000]" -c "set rp [mrw 0x08000004]" -c "reg msp $sp" -c "reg pc $rp" -c "resume" -c "shutdown"

echo.
echo Done. DS0 and DS1 should blink every 500 ms.
pause
