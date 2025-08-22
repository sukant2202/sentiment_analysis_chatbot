#!/usr/bin/env python3
"""
Setup script for SentimentBot - AI-Powered Sentiment Analysis Chatbot
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print the setup banner"""
    print("=" * 60)
    print("🤖 SentimentBot Setup Script")
    print("=" * 60)
    print("Setting up your AI-powered sentiment analysis chatbot...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    print()

def check_pip():
    """Check if pip is available"""
    print("🔍 Checking pip availability...")
    
    try:
        import pip
        print("✅ pip is available")
    except ImportError:
        print("❌ Error: pip is not available!")
        print("   Please install pip first: https://pip.pypa.io/en/stable/installation/")
        sys.exit(1)
    
    print()

def create_virtual_environment():
    """Create a virtual environment"""
    print("🔧 Creating virtual environment...")
    
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment '{venv_name}' already exists")
    else:
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
            print(f"✅ Virtual environment '{venv_name}' created successfully")
        except subprocess.CalledProcessError:
            print("❌ Error: Failed to create virtual environment")
            sys.exit(1)
    
    print()

def activate_virtual_environment():
    """Activate the virtual environment"""
    print("🔧 Activating virtual environment...")
    
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
        print(f"✅ Virtual environment ready!")
        print(f"   To activate on Windows, run: venv\\Scripts\\activate")
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        print(f"✅ Virtual environment ready!")
        print(f"   To activate on macOS/Linux, run: source venv/bin/activate")
    
    print()

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Determine the pip executable path
        if platform.system() == "Windows":
            pip_path = os.path.join("venv", "Scripts", "pip")
        else:
            pip_path = os.path.join("venv", "bin", "pip")
        
        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install dependencies")
        print("   Please activate the virtual environment first and run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print()

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    
    try:
        # Determine the python executable path
        if platform.system() == "Windows":
            python_path = os.path.join("venv", "Scripts", "python")
        else:
            python_path = os.path.join("venv", "bin", "python")
        
        # Download NLTK data
        nltk_script = """
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    print("✅ punkt tokenizer already available")
except LookupError:
    nltk.download('punkt')
    print("✅ punkt tokenizer downloaded")

try:
    nltk.data.find('corpora/vader_lexicon')
    print("✅ VADER lexicon already available")
except LookupError:
    nltk.download('vader_lexicon')
    print("✅ VADER lexicon downloaded")

try:
    nltk.data.find('corpora/stopwords')
    print("✅ stopwords already available")
except LookupError:
    nltk.download('stopwords')
    print("✅ stopwords downloaded")
"""
        
        subprocess.run([python_path, "-c", nltk_script], check=True)
        print("✅ NLTK data setup completed")
        
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to download NLTK data")
        print("   Please activate the virtual environment first and run:")
        print("   python -c \"import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')\"")
        sys.exit(1)
    
    print()

def create_startup_script():
    """Create startup scripts for different platforms"""
    print("🚀 Creating startup scripts...")
    
    if platform.system() == "Windows":
        # Windows batch file
        with open("start.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting SentimentBot...\n")
            f.write("venv\\Scripts\\activate\n")
            f.write("python app.py\n")
            f.write("pause\n")
        print("✅ Created start.bat for Windows")
        
    else:
        # Unix shell script
        with open("start.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting SentimentBot...'\n")
            f.write("source venv/bin/activate\n")
            f.write("python app.py\n")
        
        # Make executable
        os.chmod("start.sh", 0o755)
        print("✅ Created start.sh for Unix/macOS")
    
    print()

def print_next_steps():
    """Print next steps for the user"""
    print("🎉 Setup completed successfully!")
    print()
    print("📋 Next steps:")
    print()
    
    if platform.system() == "Windows":
        print("1. Activate the virtual environment:")
        print("   venv\\Scripts\\activate")
        print()
        print("2. Start the chatbot:")
        print("   python app.py")
        print("   OR")
        print("   start.bat")
    else:
        print("1. Activate the virtual environment:")
        print("   source venv/bin/activate")
        print()
        print("2. Start the chatbot:")
        print("   python app.py")
        print("   OR")
        print("   ./start.sh")
    
    print()
    print("3. Open your browser and go to: http://localhost:5000")
    print()
    print("4. Start chatting and see sentiment analysis in action!")
    print()
    print("🔧 For troubleshooting, check the README.md file")
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    check_python_version()
    check_pip()
    create_virtual_environment()
    activate_virtual_environment()
    install_dependencies()
    download_nltk_data()
    create_startup_script()
    print_next_steps()

if __name__ == "__main__":
    main()
