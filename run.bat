@echo off
REM ============================================================
REM VEGA - Run Application
REM ============================================================
REM Quick launcher for the VEGA Tally P&L Automation
REM ============================================================

echo.
echo ============================================================
echo VEGA - Tally P&L Automation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please run setup.bat first to install Python
    pause
    exit /b 1
)

REM Change to scripts directory and run
cd /d "%~dp0"
cd scripts

echo [INFO] Starting VEGA automation...
echo.

python automate.py

echo.
echo ============================================================
echo Process completed!
echo ============================================================
echo.
pause
