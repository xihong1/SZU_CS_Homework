@echo off
rem Double-click to run only (no recompile). Requires build\main.exe to exist.

cd /d "%~dp0"

if not exist build\main.exe (
    echo main.exe not found. Run build_and_run.bat first to compile.
    pause
    exit /b 1
)

build\main.exe
pause
