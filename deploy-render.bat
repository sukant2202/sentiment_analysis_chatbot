@echo off
echo 🚀 Deploying SentimentBot Pro to Render...
echo.

echo 📋 Prerequisites Check:
echo 1. Make sure you have a GitHub repository
echo 2. Make sure you have a Render account at render.com
echo.

echo 🔄 Step 1: Pushing to GitHub...
echo Please run these commands in your terminal:
echo.
echo git add .
echo git commit -m "Ready for Render deployment"
echo git push origin main
echo.

echo 🌐 Step 2: Deploy on Render
echo 1. Go to https://render.com
echo 2. Sign up/Login
echo 3. Click "New +" → "Web Service"
echo 4. Connect your GitHub repo
echo 5. Configure:
echo    - Name: sentimentbot-pro
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn index:app
echo    - Plan: Free
echo 6. Click "Create Web Service"
echo.

echo ⏳ Step 3: Wait for deployment (usually 5-10 minutes)
echo.

echo 🎉 Your app will be available at: https://sentimentbot-pro.onrender.com
echo.

pause
