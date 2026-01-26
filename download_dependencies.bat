@echo off
REM ============================================================
REM Download Dependencies for Offline Installation
REM ============================================================
REM This script downloads all Python packages as wheel files
REM for offline installation on a Windows machine without internet
REM ============================================================

echo.
echo ============================================================
echo VEGA - Downloading Dependencies for Offline Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Change to script directory
cd /d "%~dp0"

REM Create wheels directory
if not exist "wheels" mkdir wheels
echo [INFO] Created wheels directory
echo.

REM Download all dependencies as wheels
echo [INFO] Downloading dependencies as wheel files...
echo This may take a few minutes depending on your internet speed...
echo.

pip download -r requirements.txt -d wheels --no-deps

REM Download dependencies of dependencies
echo.
echo [INFO] Downloading dependency dependencies...
pip download -r requirements.txt -d wheels

echo.
echo ============================================================
echo [SUCCESS] All dependencies downloaded to 'wheels' folder
echo ============================================================
echo.
echo Next steps:
echo 1. Copy the entire VEGA folder to the target machine
echo 2. Run setup.bat on the target machine to install dependencies
echo.
pause
