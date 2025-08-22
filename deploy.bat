@echo off
echo 🚀 Deploying SentimentBot Pro to Vercel...

REM Check if vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Check if user is logged in to Vercel
vercel whoami >nul 2>&1
if errorlevel 1 (
    echo 🔐 Please log in to Vercel...
    vercel login
)

REM Deploy to Vercel
echo 📦 Deploying...
vercel --prod

echo ✅ Deployment complete!
echo 🌐 Your SentimentBot Pro is now live!
pause
