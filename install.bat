@echo off
REM ================================================================
REM  USB Device Control & Monitoring Framework — Setup Script
REM  Run this script ONCE to install all required dependencies.
REM ================================================================

echo.
echo  ===============================================================
echo    USB Device Control and Monitoring Framework - Setup
echo  ===============================================================
echo.

REM Check Python is available
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% NEQ 0 (
    echo [ERROR] Failed to install dependencies. Check your internet connection and pip setup.
    pause
    exit /b 1
)

echo.
echo [INFO] Installing optional notification library (winotify)...
pip install winotify

echo.
echo  ===============================================================
echo    Setup Complete!
echo  ===============================================================
echo.
echo  To START monitoring  (requires Admin):
echo     Right-click start_monitor.bat ^> Run as Administrator
echo.
echo  To MANAGE the policy (allowlist/blocklist):
echo     python manage_policy.py list
echo     python manage_policy.py add-allow --vid XXXX --pid YYYY
echo.
echo  To GENERATE a report from existing logs:
echo     python main.py --report
echo.
pause
