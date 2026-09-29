@echo off
setlocal


REM 获取当前脚本所在的路径
set "target_dir=%./Workspace/"

REM 检查目标文件夹是否存在，如果存在则逐个删除子文件夹
if exist "%target_dir%" (
    for /d %%i in ("%target_dir%\*") do (
        rmdir /s /q "%%i" 2>nul
    )
) 


REM 获取当前脚本所在的路径
set "script_dir=%./Workspace/"

REM 生成一个一万以内的随机数
set /a "random_num=%RANDOM% %% 1000000"

REM 构建参数中的路径
set "data_path=%script_dir%%random_num%"

REM 调用 exe 程序并传递参数
start "" /B "VDS.exe" %* -data "%data_path%"

REM 打印启动成功信息
echo Application start successful.

endlocal

