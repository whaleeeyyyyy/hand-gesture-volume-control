@echo off
echo ========================================
echo Hand Gesture Volume Control
echo ========================================
echo.

REM Check if venv exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup.bat first to create the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run app
echo Starting application...
echo.
call venv\Scripts\activate.bat && python gesture_volume_app.py

REM If app closes with error
if errorlevel 1 (
    echo.
    echo ========================================
    echo Application closed with an error!
    echo ========================================
    echo.
    pause
)