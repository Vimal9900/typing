@echo off
REM Hindi Typing Master - Startup Script for Windows

echo ======================================
echo Hindi Typing Master
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed!
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo + Python found
echo.

REM Install dependencies if needed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo + Dependencies installed
echo.

REM Run the application
echo Starting application...
echo.
echo Application will be available at:
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ======================================
echo.

python app.py
pause
