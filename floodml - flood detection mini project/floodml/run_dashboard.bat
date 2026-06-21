@echo off
REM FloodML Dashboard Launcher for Windows
REM This script runs the FloodML Streamlit dashboard

echo.
echo ============================================
echo   FloodML Dashboard Launcher
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [INFO] Python detected
python --version
echo.

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Streamlit not found. Installing dependencies...
    echo.
    pip install -r requirements-dashboard.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo Please run: pip install -r requirements-dashboard.txt
        pause
        exit /b 1
    )
)

echo [INFO] Starting FloodML Dashboard...
echo [INFO] Opening browser to http://localhost:8501
echo [INFO] Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py

pause
