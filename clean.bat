@echo off
echo ========================================
echo Clean Virtual Environment
echo ========================================
echo.
echo This will delete the virtual environment folder.
echo You'll need to run setup.bat again to reinstall.
echo.
set /p confirm="Are you sure? (Y/N): "

if /i "%confirm%"=="Y" (
    if exist venv (
        echo.
        echo Removing virtual environment...
        rmdir /s /q venv
        echo Done! Virtual environment removed.
    ) else (
        echo Virtual environment not found.
    )
) else (
    echo Cancelled.
)
echo.
pause