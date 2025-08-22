# 🚀 SentimentBot Pro - Deployment Guide

This guide covers all deployment options for your SentimentBot Pro chatbot.

## 📋 Prerequisites

- Python 3.8+
- Git
- Node.js (for Vercel deployment)
- Docker (optional, for containerized deployment)

## 🎯 Quick Start

### Windows Users
```bash
# Run the quick start script
quick-start.bat
```

### Unix/macOS Users
```bash
# Make script executable and run
chmod +x quick-start.sh
./quick-start.sh
```

## 🌐 Deployment Options

### 1. **Vercel (Recommended - Free & Easy)**

#### Setup
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login
```

#### Deploy
```bash
# Using deployment script
deploy.bat          # Windows
./deploy.sh         # Unix/macOS

# Or manually
vercel --prod
```

#### Environment Variables (set in Vercel dashboard)
- `FLASK_ENV`: `production`
- `PORT`: `5000`
- `NLTK_DATA_PATH`: `/tmp/nltk_data`

### 2. **GitHub + Vercel (Continuous Deployment)**

1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Set environment variables in Vercel dashboard
4. Every push to `main` branch auto-deploys

#### GitHub Actions (Optional)
The `.github/workflows/deploy.yml` file enables automatic deployment via GitHub Actions.

### 3. **Docker**

#### Build and Run
```bash
# Build image
docker build -t sentimentbot-pro .

# Run container
docker run -p 5000:5000 sentimentbot-pro
```

#### Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. **Traditional Server**

#### Install Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn
```

#### Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Systemd Service (Linux)
Create `/etc/systemd/system/sentimentbot.service`:
```ini
[Unit]
Description=SentimentBot Pro
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable sentimentbot
sudo systemctl start sentimentbot
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Environment (development/production)
- `PORT`: Server port (default: 5000)
- `NLTK_DATA_PATH`: Path for NLTK data
- `SECRET_KEY`: Flask secret key

### Production Settings
- Set `FLASK_ENV=production`
- Use production WSGI server (Gunicorn)
- Set up reverse proxy (Nginx/Apache)
- Configure SSL/TLS certificates
- Set up monitoring and logging

## 📊 Monitoring & Health Checks

### Health Endpoint
Your app includes a `/health` endpoint for monitoring:
```bash
curl http://your-domain/health
```

### Docker Health Check
The Dockerfile includes health checks that monitor the application status.

## 🚨 Troubleshooting

### Common Issues

#### NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"
```

#### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000    # Windows
lsof -i :5000                   # Unix/macOS

# Kill process
taskkill /PID <PID> /F          # Windows
kill -9 <PID>                   # Unix/macOS
```

#### Vercel Deployment Issues
- Check build logs in Vercel dashboard
- Ensure `vercel.json` is properly configured
- Verify environment variables are set
- Check Python runtime compatibility

### Performance Optimization
- Use production WSGI server
- Implement caching for sentiment analysis
- Consider Redis for session storage
- Optimize NLTK data loading
- Use CDN for static assets

## 🔒 Security Considerations

- Set `FLASK_ENV=production`
- Use strong `SECRET_KEY`
- Implement rate limiting
- Set up CORS properly
- Use HTTPS in production
- Regular dependency updates

## 📈 Scaling

### Horizontal Scaling
- Load balancer with multiple instances
- Session storage in Redis/database
- Stateless application design

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching layers

## 🆘 Support

- Check the main README.md for detailed setup
- Review error logs for specific issues
- Ensure all dependencies are installed
- Verify Python version compatibility

---

**Happy Deploying! 🎉**
