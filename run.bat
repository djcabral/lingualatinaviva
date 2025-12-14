@echo off
setlocal

echo ===================================================
echo   LINGUA LATINA VIVA - Windows Launcher
echo ===================================================

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 goto NoPython

REM Check/Create Virtual Environment
if exist ".venv" goto VenvExists

echo [INFO] Creating virtual environment...
python -m venv .venv
if errorlevel 1 goto VenvFail

:VenvExists
echo [INFO] Found virtual environment.

REM Activate Virtual Environment
if not exist ".venv\Scripts\activate.bat" goto ActivateFail
call .venv\Scripts\activate.bat
if errorlevel 1 goto ActivateFail

REM Install Dependencies
if not exist "requirements.txt" goto NoReqs
echo [INFO] Checking dependencies...
pip install -r requirements.txt
if errorlevel 1 echo [WARNING] Dependency install had issues.

:NoReqs

REM Run Application
echo.
echo [INFO] Starting Application...
echo.
streamlit run app.py

goto End

:NoPython
echo [ERROR] Python is not found. Please install Python 3.9+ and have it in your PATH.
echo Download: https://www.python.org/downloads/
pause
exit /b 1

:VenvFail
echo [ERROR] Failed to create virtual environment.
pause
exit /b 1

:ActivateFail
echo [ERROR] Failed to activate virtual environment. Is it corrupted?
echo Try deleting the .venv folder and running this again.
pause
exit /b 1

:End
pause
exit /b 0
