@echo off
REM ================================================================
REM  USB Device Control & Monitoring Framework - Start Monitor
REM  MUST be run as Administrator to enable device blocking.
REM ================================================================

REM CRITICAL: Change to the directory where this .bat file lives,
REM           regardless of how it was launched (including Run as Admin).
cd /d "%~dp0"

REM Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo.
    echo [ERROR] This script must be run as Administrator.
    echo         Right-click this file and choose "Run as Administrator".
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo    USB Device Control and Monitoring Framework
echo ========================================================
echo.
echo [INFO] Starting monitor... Press Ctrl+C to stop.
echo.

REM Force Python to use UTF-8 for all I/O (handles encoding without chcp)
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

python main.py

echo.
echo [INFO] Monitor stopped.
pause
