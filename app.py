from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob
import nltk
import re
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import random
from collections import defaultdict

# Load environment variables
load_dotenv()

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

# Try to import optional dependencies
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: numpy not available, some features may be limited")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available, some features may be limited")

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
    'education': ['school', 'university', 'college', 'study', 'learning', 'course', 'degree', 'student', 'teacher', 'professor', 'education', 'academic', 'research', 'knowledge', 'skill'],
    'work': ['job', 'career', 'work', 'office', 'business', 'company', 'project', 'meeting', 'colleague', 'boss', 'salary', 'promotion', 'workplace', 'professional', 'industry'],
    'relationships': ['friend', 'family', 'partner', 'relationship', 'love', 'dating', 'marriage', 'parent', 'child', 'sibling', 'romance', 'connection', 'social', 'community'],
    'finance': ['money', 'finance', 'investment', 'banking', 'budget', 'savings', 'expenses', 'income', 'tax', 'insurance', 'loan', 'credit', 'financial', 'economy', 'market'],
    'travel': ['travel', 'vacation', 'trip', 'destination', 'hotel', 'flight', 'tourism', 'adventure', 'explore', 'journey', 'culture', 'experience', 'sightseeing', 'backpacking'],
    'hobbies': ['hobby', 'interest', 'passion', 'activity', 'sport', 'music', 'art', 'reading', 'gaming', 'cooking', 'gardening', 'photography', 'crafting', 'collecting', 'outdoor'],
    'current_events': ['news', 'politics', 'world', 'society', 'environment', 'climate', 'pandemic', 'election', 'government', 'policy', 'social issues', 'global', 'current affairs'],
    'personal_development': ['growth', 'self-improvement', 'goals', 'motivation', 'success', 'happiness', 'mindset', 'productivity', 'leadership', 'confidence', 'skills', 'development', 'achievement']
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
        session_id = data.get('session_id', 'default')
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Update conversation context
        update_conversation_context(session_id, user_input)
        
        # Perform sentiment analysis using multiple methods
        sentiment_results = analyze_sentiment_comprehensive(user_input)
        
        # Detect topics from user input
        detected_topics = detect_topics(user_input)
        conversation_contexts[session_id]['topics'].update(detected_topics)
        
        # Generate contextual response with long conversation support
        response = generate_contextual_response(sentiment_results, user_input, session_id)
        
        # Generate topic suggestions
        suggestions = generate_topic_suggestions(session_id, user_input, sentiment_results)
        
        # Prepare response data
        response_data = {
            'user_message': user_input,
            'bot_response': response,
            'sentiment_analysis': sentiment_results,
            'timestamp': datetime.now().isoformat(),
            'confidence': calculate_confidence(sentiment_results),
            'detected_topics': list(detected_topics),
            'conversation_summary': get_conversation_summary(session_id),
            'suggestions': suggestions,
            'session_id': session_id
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def update_conversation_context(session_id, user_input):
    """Update conversation context with new message"""
    context = conversation_contexts[session_id]
    context['messages'].append({
        'message': user_input,
        'timestamp': datetime.now(),
        'type': 'user'
    })
    context['conversation_length'] += 1
    context['last_activity'] = datetime.now()
    
    # Keep only last 50 messages for memory management
    if len(context['messages']) > 50:
        context['messages'] = context['messages'][-50:]

def detect_topics(text):
    """Detect topics from user input text"""
    text_lower = text.lower()
    detected_topics = set()
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_topics.add(topic)
                break
    
    return detected_topics

def generate_topic_suggestions(session_id, user_input, sentiment_results):
    """Generate intelligent topic suggestions based on conversation context"""
    context = conversation_contexts[session_id]
    suggestions = []
    
    # Get current topics
    current_topics = context['topics']
    
    # Generate suggestions based on conversation length and sentiment
    if context['conversation_length'] < 5:
        # Early conversation - suggest broad topics
        suggestions.extend([
            "Tell me more about your day",
            "What are your main interests?",
            "How are you feeling about work or personal life?",
            "What's something you'd like to discuss?"
        ])
    elif context['conversation_length'] < 15:
        # Mid conversation - suggest related topics
        if 'technology' in current_topics:
            suggestions.extend([
                "What's your experience with AI and machine learning?",
                "How do you stay updated with tech trends?",
                "What's your favorite programming language or tool?"
            ])
        if 'health' in current_topics:
            suggestions.extend([
                "How do you maintain work-life balance?",
                "What's your approach to stress management?",
                "Do you have any fitness or wellness goals?"
            ])
        if 'work' in current_topics:
            suggestions.extend([
                "What's your biggest professional challenge?",
                "How do you handle workplace stress?",
                "What are your career goals for the future?"
            ])
    else:
        # Long conversation - suggest deep dive topics
        if sentiment_results['final_sentiment'] == 'positive':
            suggestions.extend([
                "This is great! What's driving your positive energy?",
                "How can you maintain this momentum?",
                "What would you like to achieve next?"
            ])
        elif sentiment_results['final_sentiment'] == 'negative':
            suggestions.extend([
                "I sense you're going through something challenging. Would you like to explore solutions?",
                "What support systems do you have in place?",
                "How can we work through this together?"
            ])
        else:
            suggestions.extend([
                "Let's dive deeper into what you're thinking about",
                "What aspects of this topic interest you most?",
                "How do you see this fitting into your broader goals?"
            ])
    
    # Add personalized suggestions based on user interests
    if context['user_interests']:
        for interest in list(context['user_interests'])[:3]:
            if interest == 'technology':
                suggestions.append("What's the most exciting tech development you've seen recently?")
            elif interest == 'health':
                suggestions.append("How do you prioritize your health in your daily routine?")
            elif interest == 'education':
                suggestions.append("What's something new you'd like to learn this year?")
    
    # Remove duplicates and limit suggestions
    unique_suggestions = list(dict.fromkeys(suggestions))
    return unique_suggestions[:5]

def get_conversation_summary(session_id):
    """Generate a summary of the current conversation"""
    context = conversation_contexts[session_id]
    
    if context['conversation_length'] == 0:
        return "Starting a new conversation"
    
    summary = {
        'total_messages': context['conversation_length'],
        'topics_discussed': list(context['topics']),
        'conversation_duration': str(datetime.now() - context['last_activity']).split('.')[0],
        'sentiment_trend': analyze_sentiment_trend(context['sentiment_history']),
        'engagement_level': get_engagement_level(context['conversation_length'])
    }
    
    return summary

def analyze_sentiment_trend(sentiment_history):
    """Analyze the trend of sentiment over the conversation"""
    if len(sentiment_history) < 2:
        return "stable"
    
    recent_sentiments = sentiment_history[-5:]  # Last 5 sentiments
    positive_count = sum(1 for s in recent_sentiments if s > 0)
    negative_count = sum(1 for s in recent_sentiments if s < 0)
    
    if positive_count > negative_count:
        return "improving"
    elif negative_count > positive_count:
        return "declining"
    else:
        return "stable"

def get_engagement_level(conversation_length):
    """Determine the level of user engagement"""
    if conversation_length < 5:
        return "low"
    elif conversation_length < 15:
        return "medium"
    elif conversation_length < 30:
        return "high"
    else:
        return "very high"

@app.route('/long_conversation', methods=['POST'])
def long_conversation():
    """Endpoint for long conversation analysis and suggestions"""
    try:
        data = request.get_json()
        if not data or 'session_id' not in data:
            return jsonify({'error': 'No session ID provided'}), 400
        
        session_id = data['session_id']
        context = conversation_contexts[session_id]
        
        # Analyze conversation patterns
        analysis = analyze_conversation_patterns(session_id)
        
        # Generate comprehensive suggestions
        comprehensive_suggestions = generate_comprehensive_suggestions(session_id, analysis)
        
        # Get conversation insights
        insights = get_conversation_insights(session_id)
        
        return jsonify({
            'conversation_analysis': analysis,
            'suggestions': comprehensive_suggestions,
            'insights': insights,
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def analyze_conversation_patterns(session_id):
    """Analyze patterns in the conversation"""
    context = conversation_contexts[session_id]
    
    if not context['messages']:
        return {"error": "No conversation data available"}
    
    # Analyze message patterns
    message_lengths = [len(msg['message']) for msg in context['messages']]
    avg_message_length = sum(message_lengths) / len(message_lengths) if message_lengths else 0
    
    # Analyze topic distribution
    topic_frequency = {}
    for topic in context['topics']:
        topic_frequency[topic] = sum(1 for msg in context['messages'] if topic in detect_topics(msg['message']))
    
    # Analyze conversation flow
    conversation_flow = "steady"
    if context['conversation_length'] > 10:
        recent_activity = context['last_activity'] - context['messages'][-10]['timestamp']
        if recent_activity.seconds < 300:  # 5 minutes
            conversation_flow = "intense"
        elif recent_activity.seconds > 1800:  # 30 minutes
            conversation_flow = "sporadic"
    
    return {
        'total_messages': context['conversation_length'],
        'average_message_length': round(avg_message_length, 1),
        'topic_distribution': topic_frequency,
        'conversation_flow': conversation_flow,
        'user_engagement': get_engagement_level(context['conversation_length']),
        'conversation_duration': str(datetime.now() - context['messages'][0]['timestamp']).split('.')[0] if context['messages'] else "0:00:00"
    }

def generate_comprehensive_suggestions(session_id, analysis):
    """Generate comprehensive suggestions based on conversation analysis"""
    context = conversation_contexts[session_id]
    suggestions = {
        'immediate': [],
        'short_term': [],
        'long_term': []
    }
    
    # Immediate suggestions (next few messages)
    if analysis['conversation_flow'] == 'intense':
        suggestions['immediate'].extend([
            "You seem very engaged! What's driving your interest in this topic?",
            "Let's take a moment to reflect on what we've discussed so far",
            "Is there a specific aspect you'd like to explore deeper?"
        ])
    elif analysis['conversation_flow'] == 'sporadic':
        suggestions['immediate'].extend([
            "I notice we're having breaks in our conversation. Is everything okay?",
            "Would you like to pick up where we left off?",
            "What would help you feel more comfortable continuing our discussion?"
        ])
    
    # Short-term suggestions (next conversation session)
    if context['conversation_length'] > 20:
        suggestions['short_term'].extend([
            "We've covered a lot of ground! Would you like to summarize your key takeaways?",
            "What questions do you still have about the topics we've discussed?",
            "How do you plan to apply what we've talked about?"
        ])
    
    # Long-term suggestions (future conversations)
    if context['topics']:
        primary_topic = max(context['topics'], key=lambda t: sum(1 for msg in context['messages'] if t in detect_topics(msg['message'])))
        suggestions['long_term'].extend([
            f"Consider exploring more about {primary_topic} in future conversations",
            "You might want to set some goals related to the topics we've discussed",
            "Think about how these discussions connect to your broader life goals"
        ])
    
    return suggestions

def get_conversation_insights(session_id):
    """Get insights about the conversation"""
    context = conversation_contexts[session_id]
    
    insights = {
        'strengths': [],
        'areas_for_growth': [],
        'recommendations': []
    }
    
    # Identify conversation strengths
    if context['conversation_length'] > 10:
        insights['strengths'].append("You're showing strong engagement in this conversation")
    
    if len(context['topics']) > 2:
        insights['strengths'].append("You're exploring diverse topics, showing intellectual curiosity")
    
    # Identify areas for growth
    if context['conversation_length'] < 5:
        insights['areas_for_growth'].append("Consider sharing more details to deepen our discussion")
    
    if not context['topics']:
        insights['areas_for_growth'].append("Try to be more specific about topics you'd like to discuss")
    
    # Generate recommendations
    if context['sentiment_history'] and len(context['sentiment_history']) > 3:
        recent_sentiment = context['sentiment_history'][-1]
        if recent_sentiment < 0:
            insights['recommendations'].append("Consider focusing on positive aspects or solutions")
        elif recent_sentiment > 0:
            insights['recommendations'].append("Great energy! Consider how to maintain this positive momentum")
    
    return insights

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

def generate_contextual_response(sentiment_results, user_input, session_id):
    """Generate contextual response based on sentiment analysis and conversation context"""
    
    sentiment = sentiment_results['final_sentiment']
    confidence = sentiment_results['confidence']
    context = conversation_contexts[session_id]
    
    # Update sentiment history
    context['sentiment_history'].append(sentiment_results['combined_score'])
    
    # Context-aware responses
    if 'how are you' in user_input.lower() or 'how do you feel' in user_input.lower():
        if sentiment == 'positive':
            return "I'm doing great, and I can sense your positive energy! How can I help you today?"
        elif sentiment == 'negative':
            return "I'm here for you. I notice you might be having a tough time. Would you like to talk about it?"
        else:
            return "I'm doing well, thank you for asking. How are you feeling today?"
    
    # Long conversation specific responses
    if context['conversation_length'] > 10:
        if sentiment == 'positive':
            return "I'm really enjoying our conversation! Your enthusiasm is contagious. What would you like to explore next?"
        elif sentiment == 'negative':
            return "We've been talking for a while, and I sense you're going through something challenging. Would you like to take a different approach or explore solutions?"
        else:
            return "We've covered quite a bit of ground. What aspects of our discussion would you like to dive deeper into?"
    
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
            'rule_based': 'active',
            'long_conversation': 'active',
            'topic_detection': 'active'
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

@app.route('/conversation_summary/<session_id>', methods=['GET'])
def get_conversation_summary_endpoint(session_id):
    """Get conversation summary for a specific session"""
    try:
        if session_id not in conversation_contexts:
            return jsonify({'error': 'Session not found'}), 404
        
        summary = get_conversation_summary(session_id)
        analysis = analyze_conversation_patterns(session_id)
        
        return jsonify({
            'session_id': session_id,
            'summary': summary,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# For Vercel deployment
app.debug = False

# Ensure CORS is properly configured for Vercel
CORS(app, origins=["*"], methods=["GET", "POST", "OPTIONS"])

# Add error handling for Vercel
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500