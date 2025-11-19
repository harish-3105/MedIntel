@echo off
REM MedIntel Quick Start Script for Windows
REM This script sets up and runs MedIntel

echo ==================================================
echo 🏥 MedIntel - Quick Start Setup
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.installed" (
    echo.
    echo 📥 Installing dependencies (this may take 5-10 minutes)...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo. > venv\.installed
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo ⚙️ Creating configuration file...
    copy .env.example .env
    echo ✅ Configuration file created
)

echo.
echo ==================================================
echo ✅ Setup Complete!
echo ==================================================
echo.
echo 🚀 Starting MedIntel server...
echo.
echo 📍 Server will be available at:
echo    - Main API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
echo ==================================================
echo.

REM Start the server
python main.py

pause
