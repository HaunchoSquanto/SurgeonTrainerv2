@echo off
setlocal

echo ========================================
echo   SurgeonTrainer Backend Startup
echo ========================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
echo Script location: %SCRIPT_DIR%
echo.

REM Change to the api directory
echo Changing to API directory...
cd /d "%SCRIPT_DIR%api"
if errorlevel 1 (
    echo ERROR: Could not find api directory at %SCRIPT_DIR%api
    pause
    exit /b 1
)
echo Current directory: %CD%
echo.

REM Check if uvicorn exists
if not exist "%SCRIPT_DIR%.venv\Scripts\uvicorn.exe" (
    echo ERROR: uvicorn.exe not found at %SCRIPT_DIR%.venv\Scripts\uvicorn.exe
    echo Please ensure the virtual environment is set up correctly.
    pause
    exit /b 1
)

echo Starting uvicorn server...
echo Command: "%SCRIPT_DIR%.venv\Scripts\uvicorn.exe" app.main:app --host 127.0.0.1 --port 8000 --reload
echo.
"%SCRIPT_DIR%.venv\Scripts\uvicorn.exe" app.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo Server stopped.
pause
