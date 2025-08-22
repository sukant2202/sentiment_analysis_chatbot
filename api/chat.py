from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import nltk
import json
from datetime import datetime
import os
import random
from collections import defaultdict

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
CORS(app)

# Set NLTK data path for Vercel
NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH', '/tmp/nltk_data')
nltk.data.path.append(NLTK_DATA_PATH)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/vader_lexicon')
    nltk.data.find('corpora/stopwords')
except LookupError:
    print(f"Downloading NLTK data to {NLTK_DATA_PATH}...")
    nltk.download('punkt', download_dir=NLTK_DATA_PATH)
    nltk.download('vader_lexicon', download_dir=NLTK_DATA_PATH)
    nltk.download('stopwords', download_dir=NLTK_DATA_PATH)
    print("NLTK data download complete.")

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

# Topic detection keywords and categories
TOPIC_KEYWORDS = {
    'technology': ['computer', 'software', 'programming', 'ai', 'machine learning', 'data', 'internet', 'app', 'digital', 'tech', 'code', 'algorithm', 'database', 'cloud', 'cybersecurity'],
    'health': ['health', 'medical', 'doctor', 'hospital', 'medicine', 'symptoms', 'treatment', 'exercise', 'diet', 'nutrition', 'fitness', 'wellness', 'mental health', 'therapy', 'recovery'],
    'work': ['job', 'career', 'work', 'office', 'business', 'company', 'project', 'meeting', 'colleague', 'boss', 'salary', 'promotion', 'workplace', 'professional', 'industry'],
    'relationships': ['friend', 'family', 'partner', 'relationship', 'love', 'dating', 'marriage', 'parent', 'child', 'sibling', 'romance', 'connection', 'social', 'community']
}

# Conversation context and topic tracking
conversation_contexts = defaultdict(lambda: {
    'messages': [],
    'topics': set(),
    'sentiment_history': [],
    'conversation_length': 0,
    'last_activity': datetime.now(),
    'user_interests': set(),
    'suggested_topics': []
})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_input = data['message'].strip()
        session_id = data.get('session_id', 'default')
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Analyze sentiment
        sentiment_results = analyze_sentiment_comprehensive(user_input)
        
        # Generate response
        bot_response = generate_contextual_response(sentiment_results, user_input, session_id)
        
        # Update conversation context
        update_conversation_context(session_id, user_input)
        
        # Detect topics
        detected_topics = detect_topics(user_input)
        conversation_contexts[session_id]['topics'].update(detected_topics)
        
        # Generate suggestions
        suggestions = generate_topic_suggestions(session_id, user_input, sentiment_results)
        
        return jsonify({
            'user_message': user_input,
            'bot_response': bot_response,
            'sentiment_analysis': sentiment_results,
            'timestamp': datetime.now().isoformat(),
            'confidence': calculate_confidence(sentiment_results),
            'detected_topics': list(detected_topics),
            'conversation_summary': get_conversation_summary(session_id),
            'suggestions': suggestions,
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def analyze_sentiment_comprehensive(text):
    """Comprehensive sentiment analysis using multiple methods"""
    # TextBlob analysis
    blob = TextBlob(text)
    textblob_score = blob.sentiment.polarity
    
    # VADER analysis
    vader_scores = vader_analyzer.polarity_scores(text)
    vader_score = vader_scores['compound']
    
    # Keyword analysis
    keyword_score = analyze_keywords(text)
    
    # Rule-based analysis
    rule_score = rule_based_sentiment(text)
    
    # Calculate weighted average
    weights = [0.3, 0.4, 0.2, 0.1]  # TextBlob, VADER, Keywords, Rules
    combined_score = (
        textblob_score * weights[0] +
        vader_score * weights[1] +
        keyword_score * weights[2] +
        rule_score * weights[3]
    )
    
    # Determine sentiment
    if combined_score > 0.1:
        sentiment = 'positive'
    elif combined_score < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'sentiment': sentiment,
        'combined_score': combined_score,
        'confidence': abs(combined_score),
        'breakdown': {
            'textblob': textblob_score,
            'vader': vader_score,
            'keywords': keyword_score,
            'rules': rule_score
        }
    }

def analyze_keywords(text):
    """Analyze sentiment based on keyword presence"""
    words = set(word.lower() for word in word_tokenize(text))
    positive_count = len(words.intersection(POSITIVE_WORDS))
    negative_count = len(words.intersection(NEGATIVE_WORDS))
    
    if positive_count > negative_count:
        return 0.5
    elif negative_count > positive_count:
        return -0.5
    else:
        return 0.0

def rule_based_sentiment(text):
    """Rule-based sentiment analysis"""
    score = 0.0
    
    # Exclamation marks
    if text.count('!') > 0:
        score += 0.1 * text.count('!')
    
    # Emoticons
    positive_emoticons = [':)', ':-)', '😊', '😄', '😍', '👍', '❤️']
    negative_emoticons = [':(', ':-(', '😢', '😭', '😡', '👎', '💔']
    
    for emoticon in positive_emoticons:
        if emoticon in text:
            score += 0.3
    
    for emoticon in negative_emoticons:
        if emoticon in text:
            score -= 0.3
    
    # Capitalization (all caps = emphasis)
    if text.isupper() and len(text) > 3:
        score += 0.2
    
    return max(-1.0, min(1.0, score))

def generate_contextual_response(sentiment_results, user_input, session_id):
    """Generate contextual response based on sentiment and conversation"""
    sentiment = sentiment_results['sentiment']
    confidence = sentiment_results['confidence']
    
    # Simple response generation
    if sentiment == 'positive':
        responses = [
            "That's wonderful! Your positive energy is contagious. 😊",
            "I'm so glad to hear that! It sounds like things are going well for you.",
            "That's fantastic! Your enthusiasm really comes through in your message."
        ]
    elif sentiment == 'negative':
        responses = [
            "I'm sorry to hear that you're feeling this way. Remember, it's okay to not be okay.",
            "I can sense that you're going through a difficult time. Would you like to talk more about it?",
            "I'm here to listen. Sometimes talking about our feelings can help us feel better."
        ]
    else:
        responses = [
            "I see you're being quite neutral about this. Would you like to elaborate?",
            "Interesting perspective. I'd love to hear more about your thoughts on this.",
            "Thanks for sharing. I'd like to understand your perspective better."
        ]
    
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

def update_conversation_context(session_id, user_input):
    """Update conversation context for a session"""
    context = conversation_contexts[session_id]
    context['messages'].append({
        'text': user_input,
        'timestamp': datetime.now().isoformat()
    })
    context['conversation_length'] += 1
    context['last_activity'] = datetime.now()

def detect_topics(text):
    """Detect topics from user input"""
    text_lower = text.lower()
    detected_topics = set()
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_topics.add(topic)
                break
    
    return detected_topics

def generate_topic_suggestions(session_id, user_input, sentiment_results):
    """Generate topic suggestions based on conversation"""
    context = conversation_contexts[session_id]
    suggestions = []
    
    if context['conversation_length'] < 3:
        suggestions.append("Tell me more about your day")
        suggestions.append("What's on your mind lately?")
    else:
        for topic in context['topics']:
            if topic == 'technology':
                suggestions.append("What's your favorite tech gadget?")
            elif topic == 'health':
                suggestions.append("How do you stay healthy?")
            elif topic == 'work':
                suggestions.append("What do you enjoy most about your work?")
    
    return suggestions[:3]

def get_conversation_summary(session_id):
    """Get conversation summary for a session"""
    context = conversation_contexts[session_id]
    return {
        'message_count': context['conversation_length'],
        'topics': list(context['topics']),
        'last_activity': context['last_activity'].isoformat()
    }

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

# For Vercel deployment
app.debug = False

# Add error handling for Vercel
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
