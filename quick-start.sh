#!/bin/bash

echo "🚀 SentimentBot Pro - Quick Start"
echo "================================"

echo
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip"
    exit 1
fi

echo "✅ Python and pip found!"

echo
echo "🔧 Setting up virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo
echo "🧠 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"

echo
echo "🎉 Setup complete! Starting SentimentBot Pro..."
echo "🌐 Open http://localhost:5000 in your browser"
echo
echo "Press Ctrl+C to stop the server"
echo

python app.py
