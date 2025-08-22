@echo off
echo 🚀 SentimentBot Pro - Quick Start
echo ================================

echo.
echo 📋 Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not found. Please install pip
    pause
    exit /b 1
)

echo ✅ Python and pip found!

echo.
echo 🔧 Setting up virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🧠 Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"

echo.
echo 🎉 Setup complete! Starting SentimentBot Pro...
echo 🌐 Open http://localhost:5000 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
