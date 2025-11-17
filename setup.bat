@echo off
echo ========================================
echo Hand Gesture Volume Control - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please download Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
python --version

echo.
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Installing dependencies...
echo This may take a few minutes...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed!
    echo Try running: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Virtual environment created at: venv\
echo All dependencies installed successfully!
echo.
echo To run the app:
echo   - Double-click: run.bat
echo   - Or manually: venv\Scripts\python.exe gesture_volume_app.py
echo.
pause