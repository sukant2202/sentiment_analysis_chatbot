#!/bin/bash

echo "🚀 Deploying SentimentBot Pro to Vercel..."
echo

echo "📋 Checking prerequisites..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI"
        exit 1
    fi
fi

echo "✅ Vercel CLI found"
echo

echo "🔐 Logging in to Vercel..."
vercel login
if [ $? -ne 0 ]; then
    echo "❌ Failed to login to Vercel"
    exit 1
fi

echo
echo "🚀 Deploying to Vercel..."
vercel --prod

echo
echo "✅ Deployment complete!"
echo "📱 Check your Vercel dashboard for the live URL"
echo
