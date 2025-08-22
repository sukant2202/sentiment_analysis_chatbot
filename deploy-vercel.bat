@echo off
echo 🚀 Deploying SentimentBot Pro to Vercel...
echo.

echo 📋 Checking prerequisites...
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Vercel CLI. Please install Node.js first.
        pause
        exit /b 1
    )
)

echo ✅ Vercel CLI found
echo.

echo 🔐 Logging in to Vercel...
vercel login
if %errorlevel% neq 0 (
    echo ❌ Failed to login to Vercel
    pause
    exit /b 1
)

echo.
echo 🚀 Deploying to Vercel...
vercel --prod

echo.
echo ✅ Deployment complete!
echo 📱 Check your Vercel dashboard for the live URL
echo.
pause
