from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob
import nltk
import re
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/vader_lexicon')
except LookupError:
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('stopwords')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Initialize sentiment analyzers
vader_analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

# Sentiment keywords for enhanced analysis
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
    'happy', 'joy', 'love', 'like', 'enjoy', 'pleased', 'satisfied', 'perfect',
    'beautiful', 'nice', 'wonderful', 'brilliant', 'outstanding', 'superb'
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike',
    'sad', 'angry', 'frustrated', 'disappointed', 'upset', 'worried', 'anxious',
    'depressed', 'miserable', 'painful', 'suffering', 'terrible', 'dreadful'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_input = data['message'].strip()
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Perform sentiment analysis using multiple methods
        sentiment_results = analyze_sentiment_comprehensive(user_input)
        
        # Generate contextual response
        response = generate_contextual_response(sentiment_results, user_input)
        
        # Prepare response data
        response_data = {
            'user_message': user_input,
            'bot_response': response,
            'sentiment_analysis': sentiment_results,
            'timestamp': datetime.now().isoformat(),
            'confidence': calculate_confidence(sentiment_results)
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def analyze_sentiment_comprehensive(text):
    """Perform comprehensive sentiment analysis using multiple methods"""
    
    # Method 1: TextBlob
    textblob_analysis = TextBlob(text)
    textblob_sentiment = textblob_analysis.sentiment
    
    # Method 2: VADER
    vader_scores = vader_analyzer.polarity_scores(text)
    
    # Method 3: Keyword-based analysis
    keyword_sentiment = analyze_keywords(text)
    
    # Method 4: Rule-based analysis
    rule_based = rule_based_sentiment(text)
    
    # Combine results
    combined_score = (
        textblob_sentiment.polarity * 0.3 +
        vader_scores['compound'] * 0.4 +
        keyword_sentiment * 0.2 +
        rule_based * 0.1
    )
    
    # Determine final sentiment
    if combined_score > 0.1:
        final_sentiment = 'positive'
    elif combined_score < -0.1:
        final_sentiment = 'negative'
    else:
        final_sentiment = 'neutral'
    
    return {
        'final_sentiment': final_sentiment,
        'combined_score': combined_score,
        'textblob': {
            'polarity': textblob_sentiment.polarity,
            'subjectivity': textblob_sentiment.subjectivity
        },
        'vader': vader_scores,
        'keyword_based': keyword_sentiment,
        'rule_based': rule_based,
        'confidence': abs(combined_score)
    }

def analyze_keywords(text):
    """Analyze sentiment based on keyword presence"""
    text_lower = text.lower()
    words = word_tokenize(text_lower)
    
    positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    if positive_count > negative_count:
        return 0.5
    elif negative_count > positive_count:
        return -0.5
    else:
        return 0.0

def rule_based_sentiment(text):
    """Simple rule-based sentiment analysis"""
    text_lower = text.lower()
    
    # Exclamation marks
    exclamation_count = text.count('!')
    
    # Question marks
    question_count = text.count('?')
    
    # Capital letters (shouting)
    capital_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
    
    # Emoticons
    positive_emoticons = [':)', ':-)', '😊', '😄', '😃', '😀', '😁', '😆', '😅', '🤗']
    negative_emoticons = [':(', ':-(', '😢', '😭', '😞', '😔', '😟', '😕', '😣', '😖']
    
    positive_emoticon_count = sum(text.count(emoticon) for emoticon in positive_emoticons)
    negative_emoticon_count = sum(text.count(emoticon) for emoticon in negative_emoticons)
    
    score = 0
    score += exclamation_count * 0.1
    score += (positive_emoticon_count - negative_emoticon_count) * 0.3
    score += capital_ratio * 0.2
    
    return max(-1.0, min(1.0, score))

def generate_contextual_response(sentiment_results, user_input):
    """Generate contextual response based on sentiment analysis"""
    
    sentiment = sentiment_results['final_sentiment']
    confidence = sentiment_results['confidence']
    
    # Context-aware responses
    if 'how are you' in user_input.lower() or 'how do you feel' in user_input.lower():
        if sentiment == 'positive':
            return "I'm doing great, and I can sense your positive energy! How can I help you today?"
        elif sentiment == 'negative':
            return "I'm here for you. I notice you might be having a tough time. Would you like to talk about it?"
        else:
            return "I'm doing well, thank you for asking. How are you feeling today?"
    
    # Sentiment-specific responses
    if sentiment == 'positive':
        responses = [
            "That's wonderful! Your positive energy is contagious. 😊",
            "I'm so glad to hear that! It sounds like things are going well for you.",
            "That's fantastic! Your enthusiasm really comes through in your message.",
            "Wonderful! I can feel your positive vibes. Keep that energy going! ✨"
        ]
    elif sentiment == 'negative':
        responses = [
            "I'm sorry to hear that you're feeling this way. Remember, it's okay to not be okay.",
            "I can sense that you're going through a difficult time. Would you like to talk more about it?",
            "I'm here to listen. Sometimes talking about our feelings can help us feel better.",
            "I understand this is tough. Remember that difficult times are temporary, and you're not alone."
        ]
    else:
        responses = [
            "I see you're being quite neutral about this. Would you like to elaborate?",
            "Interesting perspective. I'd love to hear more about your thoughts on this.",
            "I'm curious to know more about how you feel. Care to share?",
            "Thanks for sharing. I'd like to understand your perspective better."
        ]
    
    import random
    return random.choice(responses)

def calculate_confidence(sentiment_results):
    """Calculate confidence level of sentiment analysis"""
    confidence = sentiment_results['confidence']
    
    if confidence > 0.7:
        return 'high'
    elif confidence > 0.4:
        return 'medium'
    else:
        return 'low'

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'textblob': 'active',
            'vader': 'active',
            'keyword_analysis': 'active',
            'rule_based': 'active'
        }
    })

@app.route('/sentiment', methods=['POST'])
def analyze_sentiment_only():
    """Endpoint for sentiment analysis only"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        sentiment_results = analyze_sentiment_comprehensive(text)
        
        return jsonify({
            'text': text,
            'sentiment_analysis': sentiment_results
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)