@echo off
setlocal

echo ===================================================
echo   LINGUA LATINA VIVA - Windows Launcher
echo ===================================================

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found. Please install Python 3.9+ and add it to PATH.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check/Create Virtual Environment
if not exist ".venv" (
    echo [INFO] Creating virtual environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Found existing virtual environment.
)

REM Activate Virtual Environment
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install Dependencies
if exist "requirements.txt" (
    echo [INFO] Checking dependencies...
    pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found! Skipping dependency install.
)

REM Run Application
echo.
echo [INFO] Starting Application...
echo.
streamlit run app.py

pause
