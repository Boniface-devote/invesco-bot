@echo off
echo Opening Invesco Form with Extracted Data...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if client_automation.py exists
if not exist "client_automation.py" (
    echo Error: client_automation.py not found
    echo Please ensure the file is in the same directory
    pause
    exit /b 1
)

REM Run the client automation
python client_automation.py

pause
