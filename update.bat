@echo off
REM Neuron Automation Update Script Wrapper for Windows
REM ====================================================

setlocal

set "SCRIPT_DIR=%~dp0"
set "UPDATE_SCRIPT=%SCRIPT_DIR%update.py"

echo 🔄 Neuron Automation Update Utility
echo ====================================

REM Check if Python script exists
if not exist "%UPDATE_SCRIPT%" (
    echo ❌ Update script not found: %UPDATE_SCRIPT%
    exit /b 1
)

REM Check Python availability
python --version >nul 2>&1
if %errorlevel% == 0 (
    set "PYTHON_CMD=python"
    goto :run_update
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set "PYTHON_CMD=python3"
    goto :run_update
)

echo ❌ Python not found. Please install Python 3.6+ to use the updater.
exit /b 1

:run_update
REM Run the update script with all arguments
"%PYTHON_CMD%" "%UPDATE_SCRIPT%" %*