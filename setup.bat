@echo off
REM ============================================================
REM VEGA - Offline Setup Script
REM ============================================================
REM This script sets up the VEGA application on a Windows machine
REM without internet connectivity
REM ============================================================

echo.
echo ============================================================
echo VEGA - Offline Setup and Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8 or higher:
    echo 1. Download Python from: https://www.python.org/downloads/
    echo 2. During installation, check "Add Python to PATH"
    echo 3. Run this setup script again
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if wheels directory exists
if not exist "wheels" (
    echo [ERROR] 'wheels' directory not found!
    echo.
    echo The offline package is incomplete.
    echo Please ensure you have copied the entire VEGA folder including the 'wheels' directory.
    echo.
    pause
    exit /b 1
)

echo [OK] Wheels directory found
echo.

REM Install packages from wheels (offline)
echo [INFO] Installing Python packages from local wheels...
echo This may take a few minutes...
echo.

pip install --no-index --find-links wheels -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [SUCCESS] Setup completed successfully!
echo ============================================================
echo.
echo VEGA is now ready to use!
echo.
echo To run the application:
echo   - Double-click 'run.bat' or
echo   - Run: python scripts\automate.py
echo.
echo ============================================================
pause
