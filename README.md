# SentimentBot - AI-Powered Sentiment Analysis Chatbot

A sophisticated chatbot equipped with advanced sentiment analysis capabilities that can understand and respond to user emotions in real-time.

## 🚀 Features

### Core Capabilities
- **Multi-Model Sentiment Analysis**: Combines TextBlob, VADER, keyword-based, and rule-based analysis
- **Real-time Sentiment Visualization**: Interactive dashboard showing sentiment scores and confidence levels
- **Context-Aware Responses**: Bot responds differently based on detected sentiment and context
- **Advanced NLP Processing**: Uses NLTK for enhanced text analysis
- **Responsive Web Interface**: Modern, mobile-friendly UI with real-time updates

### Sentiment Analysis Methods
1. **TextBlob**: Polarity and subjectivity analysis
2. **VADER**: Valence Aware Dictionary and sEntiment Reasoner
3. **Keyword Analysis**: Custom positive/negative word detection
4. **Rule-based Analysis**: Emoticon, punctuation, and capitalization analysis

### Technical Features
- **Flask Backend**: RESTful API with error handling
- **Real-time Updates**: WebSocket-like experience with fetch API
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modular Architecture**: Easy to extend and customize
- **Health Monitoring**: Built-in health check endpoints

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd sentiment_analysis_chatbot
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"
```

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
sentiment_analysis_chatbot/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # Frontend templates
│   ├── index.html      # Main HTML page
│   ├── styles.css      # CSS styling
│   └── script.js       # JavaScript functionality
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### Environment Variables
You can customize the behavior using environment variables:

```bash
# Flask Configuration
export FLASK_ENV=development
export FLASK_DEBUG=True
export PORT=5000
export HOST=0.0.0.0

# Sentiment Analysis Weights
export TEXTBLOB_WEIGHT=0.3
export VADER_WEIGHT=0.4
export KEYWORD_WEIGHT=0.2
export RULE_BASED_WEIGHT=0.1

# Confidence Threshold
export SENTIMENT_CONFIDENCE_THRESHOLD=0.1
```

### Configuration File
Edit `config.py` to modify:
- Sentiment keywords
- Response templates
- Context patterns
- Model weights

## 🎯 Usage Examples

### Basic Chat
1. Open your browser and navigate to `http://localhost:5000`
2. Type a message in the chat input
3. The bot will analyze the sentiment and respond accordingly
4. View real-time sentiment analysis in the right panel

### Test Messages
Try these example messages to see different sentiment responses:

**Positive Sentiment:**
- "I'm feeling absolutely amazing today! Everything is going perfectly! 😊"
- "I love this new restaurant! The food is incredible and the service is outstanding!"

**Negative Sentiment:**
- "I'm having such a terrible day. Nothing is working out for me."
- "I hate this job so much. I'm so frustrated and angry all the time."

**Neutral Sentiment:**
- "The weather is okay, I guess. Not too bad, not too good."
- "I'm just checking in to see how things are going."

### API Endpoints

#### Chat Endpoint
```bash
POST /chat
Content-Type: application/json

{
    "message": "I'm feeling great today!"
}
```

#### Sentiment Analysis Only
```bash
POST /sentiment
Content-Type: application/json

{
    "text": "I'm feeling great today!"
}
```

#### Health Check
```bash
GET /health
```

## 🧠 How It Works

### Sentiment Analysis Pipeline
1. **Text Preprocessing**: Tokenization, stop word removal
2. **Multi-Model Analysis**: 
   - TextBlob: Polarity and subjectivity
   - VADER: Compound sentiment score
   - Keywords: Custom word detection
   - Rules: Emoticons, punctuation analysis
3. **Score Combination**: Weighted average of all methods
4. **Classification**: Positive (>0.1), Negative (<-0.1), Neutral (otherwise)
5. **Response Generation**: Context-aware, sentiment-specific responses

### Confidence Calculation
- **High Confidence**: >0.7 (Strong sentiment signals)
- **Medium Confidence**: 0.4-0.7 (Moderate sentiment signals)
- **Low Confidence**: <0.4 (Weak or conflicting signals)

## 🎨 Customization

### Adding New Sentiment Keywords
Edit `config.py` to add new positive/negative words:

```python
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
    # Add your custom positive words here
    'ecstatic', 'thrilled', 'delighted'
}
```

### Custom Response Templates
Modify response patterns in `config.py`:

```python
RESPONSE_TEMPLATES = {
    'positive': [
        "That's wonderful! Your positive energy is contagious. 😊",
        # Add your custom positive responses
        "Fantastic! You're absolutely right!"
    ]
}
```

### Adjusting Model Weights
Change the importance of different analysis methods:

```python
TEXTBLOB_WEIGHT = 0.4      # Increase TextBlob influence
VADER_WEIGHT = 0.3         # Decrease VADER influence
KEYWORD_WEIGHT = 0.2       # Keep keyword analysis
RULE_BASED_WEIGHT = 0.1    # Keep rule-based analysis
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up reverse proxy (Nginx, Apache)
4. Configure environment variables

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🧪 Testing

### Manual Testing
1. Start the application
2. Open multiple browser tabs
3. Send various message types
4. Verify sentiment analysis accuracy
5. Test error handling with invalid inputs

### Automated Testing
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

## 🔍 Troubleshooting

### Common Issues

**NLTK Data Not Found:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"
```

**Port Already in Use:**
```bash
# Change port in config.py or set environment variable
export PORT=5001
```

**Dependencies Installation Issues:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with specific versions
pip install -r requirements.txt --force-reinstall
```

### Performance Optimization
- Use production WSGI server for high traffic
- Implement caching for repeated sentiment analysis
- Consider using Redis for session storage
- Optimize NLTK data loading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TextBlob**: Simple text processing library
- **NLTK**: Natural Language Toolkit
- **VADER**: Valence Aware Dictionary and sEntiment Reasoner
- **Flask**: Web framework for Python
- **Font Awesome**: Icons and symbols

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the configuration options
3. Open an issue on GitHub
4. Check the console for error messages

## 🔮 Future Enhancements

- **Machine Learning Models**: Integration with BERT, RoBERTa
- **Multi-language Support**: Sentiment analysis in different languages
- **Emotion Detection**: More granular emotion classification
- **Voice Integration**: Speech-to-text and text-to-speech
- **Analytics Dashboard**: User interaction statistics
- **API Rate Limiting**: Production-ready API management
- **WebSocket Support**: Real-time bidirectional communication

---

**Happy Chatting! 🤖✨**
