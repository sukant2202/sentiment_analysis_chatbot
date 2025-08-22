# SentimentBot Pro - AI-Powered Sentiment Analysis & Long Conversation Chatbot

An advanced AI chatbot that combines sentiment analysis with intelligent long conversation support, built with Flask and modern web technologies.

## 🌟 Features

- **Multi-Method Sentiment Analysis**: Uses TextBlob, VADER, keyword analysis, and rule-based methods
- **Long Conversation Support**: Tracks conversation context, topics, and provides intelligent suggestions
- **Real-time Analysis**: Instant sentiment scoring with confidence levels
- **Topic Detection**: Automatically identifies and tracks conversation topics
- **Modern UI**: Beautiful, responsive interface with real-time updates
- **Session Management**: Maintains conversation context across interactions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for Vercel deployment)

### Local Development
```bash
# Clone the repository
git clone <your-repo-url>
cd sentiment_analysis_chatbot

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open http://localhost:5000 in your browser
```

## 🌐 Deployment

### Vercel Deployment (Recommended)

#### Option 1: Using Deployment Scripts
```bash
# Windows
deploy-vercel.bat

# Unix/macOS
./deploy-vercel.sh
```

#### Option 2: Manual Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Option 3: GitHub Integration
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Automatic deployment on every push

### Other Deployment Options
- **Docker**: Use `docker-compose up -d`
- **Traditional Server**: Use `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

## 🧪 Testing

Run the test suite to ensure everything works:
```bash
python test_vercel.py
```

## 📁 Project Structure

```
sentiment_analysis_chatbot/
├── app.py                 # Main Flask application
├── vercel_app.py          # Vercel entry point
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
├── static/                # CSS, JS, and static assets
├── deploy-vercel.bat     # Windows deployment script
├── deploy-vercel.sh      # Unix deployment script
└── DEPLOYMENT.md          # Detailed deployment guide
```

## 🔧 Configuration

### Environment Variables
- `NLTK_DATA_PATH`: Path for NLTK data (default: `/tmp/nltk_data`)
- `FLASK_ENV`: Environment setting (development/production)

### NLTK Data
The app automatically downloads required NLTK data:
- punkt (tokenization)
- vader_lexicon (sentiment analysis)
- stopwords (text processing)

## 📊 API Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Send message and get response
- `GET /health` - Health check
- `POST /sentiment` - Sentiment analysis only
- `POST /long_conversation` - Long conversation analysis
- `GET /conversation_summary/<session_id>` - Get conversation summary

## 🎯 Use Cases

- **Customer Support**: Analyze customer sentiment in real-time
- **Social Media Monitoring**: Track sentiment trends
- **Mental Health Support**: Provide empathetic responses
- **Educational Chatbots**: Engage students in meaningful conversations
- **Business Intelligence**: Analyze communication patterns

## 🚨 Important Notes

- **Serverless Environment**: Designed for Vercel's serverless functions
- **Memory Limitations**: Conversation context resets on each deployment
- **Timeout**: Vercel has a 10-second timeout for serverless functions
- **NLTK Data**: Automatically downloaded to `/tmp` directory

## 🔒 Security

- CORS enabled for cross-origin requests
- Input validation and sanitization
- Error handling for malformed requests
- Rate limiting considerations for production

## 📈 Performance

- Optimized for serverless deployment
- Efficient NLTK data caching
- Minimal memory footprint
- Fast response times (< 1 second typical)

## 🆘 Support

- Check the `/health` endpoint for system status
- Review Vercel function logs for debugging
- Ensure all dependencies are properly installed
- Verify Python version compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Chatting! 🎉**
