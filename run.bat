@echo off
title AI极速光轮 - 启动脚本
echo 正在启动AI极速光轮游戏...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖包...
pip show pygame >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
)

echo 启动游戏...
python main.py

pause
