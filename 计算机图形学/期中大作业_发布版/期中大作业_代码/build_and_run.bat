@echo off
rem One-click build & run for the OpenGL project (ASCII only to avoid codepage issues)

setlocal
set "GPP=D:\x86_64-8.1.0-release-win32-seh-rt_v6-rev0\mingw64\bin\g++.exe"

cd /d "%~dp0"
mkdir build
echo ===== Compiling =====
"%GPP%" -g src\glad.c src\InitShader.cpp src\main.cpp -o build\main.exe -I include -L lib -lglfw3 -lgdi32 -lopengl32

if errorlevel 1 (
    echo.
    echo ===== Build FAILED, see errors above =====
    pause
    exit /b 1
)

echo ===== Build OK, launching =====
build\main.exe

echo.
echo ===== Program exited =====
pause
endlocal
