from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import os
import re
import random
from datetime import datetime

# Create Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

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

def analyze_sentiment_comprehensive(text):
    """Perform comprehensive sentiment analysis using multiple methods"""
    
    # Method 1: Keyword-based analysis
    keyword_sentiment = analyze_keywords(text)
    
    # Method 2: Rule-based analysis
    rule_based = rule_based_sentiment(text)
    
    # Method 3: Emoticon analysis
    emoticon_sentiment = analyze_emoticons(text)
    
    # Method 4: Punctuation analysis
    punctuation_sentiment = analyze_punctuation(text)
    
    # Combine results with weights
    combined_score = (
        keyword_sentiment * 0.4 +
        rule_based * 0.3 +
        emoticon_sentiment * 0.2 +
        punctuation_sentiment * 0.1
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
        'combined_score': round(combined_score, 3),
        'keyword_based': round(keyword_sentiment, 3),
        'rule_based': round(rule_based, 3),
        'emoticon_based': round(emoticon_sentiment, 3),
        'punctuation_based': round(punctuation_sentiment, 3),
        'confidence': round(abs(combined_score), 3)
    }

def analyze_keywords(text):
    """Analyze sentiment based on keyword presence"""
    text_lower = text.lower()
    words = text_lower.split()
    
    positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
    negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    if positive_count > negative_count:
        return 0.6
    elif negative_count > positive_count:
        return -0.6
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
    
    score = 0
    score += exclamation_count * 0.1
    score += capital_ratio * 0.2
    
    return max(-1.0, min(1.0, score))

def analyze_emoticons(text):
    """Analyze sentiment based on emoticons"""
    positive_emoticons = [':)', ':-)', '😊', '😄', '😃', '😀', '😁', '😆', '😅', '🤗', '❤️', '💕', '💖', '💝']
    negative_emoticons = [':(', ':-(', '😢', '😭', '😞', '😔', '😟', '😕', '😣', '😖', '💔', '😡', '😠', '😤']
    
    positive_count = sum(text.count(emoticon) for emoticon in positive_emoticons)
    negative_count = sum(text.count(emoticon) for emoticon in negative_emoticons)
    
    if positive_count > negative_count:
        return 0.5
    elif negative_count > positive_count:
        return -0.5
    else:
        return 0.0

def analyze_punctuation(text):
    """Analyze sentiment based on punctuation patterns"""
    score = 0
    
    # Multiple exclamation marks
    if '!!!' in text or '!!' in text:
        score += 0.3
    
    # Multiple question marks
    if '???' in text or '??' in text:
        score += 0.1
    
    # Ellipsis (can indicate thoughtfulness or uncertainty)
    if '...' in text:
        score += 0.05
    
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
    
    return random.choice(responses)

# Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SentimentBot Pro - AI-Powered Sentiment Analysis & Long Conversation Chatbot</title>
        <link rel="stylesheet" href="/static/styles.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body>
        <div class="container">
            <header class="header">
                <div class="header-content">
                    <h1><i class="fas fa-robot"></i> SentimentBot Pro</h1>
                    <p>Advanced AI chatbot with sentiment analysis & intelligent long conversation support</p>
                </div>
            </header>

            <main class="main-content">
                <div class="chat-container">
                    <div class="chat-header">
                        <h2><i class="fas fa-comments"></i> Chat</h2>
                        <div class="status-indicator" id="statusIndicator">
                            <span class="status-dot"></span>
                            <span class="status-text">Ready</span>
                        </div>
                    </div>

                    <div class="chat-messages" id="chatMessages">
                        <div class="welcome-message">
                            <div class="bot-avatar">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="message-content">
                                <p>Hello! I'm SentimentBot Pro, your AI companion with advanced sentiment analysis and long conversation capabilities. I can understand how you're feeling, track our conversation topics, and provide intelligent suggestions to keep our discussions engaging and meaningful. How are you today?</p>
                                <div class="message-timestamp">Just now</div>
                            </div>
                        </div>
                    </div>

                    <div class="chat-input-container">
                        <div class="input-wrapper">
                            <input type="text" id="userInput" placeholder="Type your message here..." />
                            <button id="sendButton" class="send-button">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        <div class="input-hint">
                            <i class="fas fa-lightbulb"></i>
                            Try: "I'm feeling great today!" or start a long conversation about technology, health, work, or any topic you're passionate about
                        </div>
                    </div>
                </div>

                <div class="side-panels">
                    <!-- Sentiment Analysis Panel -->
                    <div class="sentiment-panel" id="sentimentPanel">
                        <div class="panel-header">
                            <h3><i class="fas fa-chart-line"></i> Sentiment Analysis</h3>
                            <button class="panel-toggle" id="sentimentPanelToggle">
                                <i class="fas fa-chevron-down"></i>
                            </button>
                        </div>
                        
                        <div class="panel-content" id="sentimentPanelContent">
                            <div class="sentiment-overview">
                                <div class="sentiment-score">
                                    <div class="score-circle" id="scoreCircle">
                                        <span class="score-text" id="scoreText">-</span>
                                    </div>
                                    <div class="score-label">
                                        <span class="sentiment-label" id="sentimentLabel">Neutral</span>
                                        <span class="confidence-label" id="confidenceLabel">-</span>
                                    </div>
                                </div>
                                
                                <div class="sentiment-breakdown">
                                    <h4>Analysis Breakdown</h4>
                                    <div class="breakdown-item">
                                        <span class="method-name">Keywords</span>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="keywordProgress"></div>
                                        </div>
                                        <span class="method-score" id="keywordScore">-</span>
                                    </div>
                                    
                                    <div class="breakdown-item">
                                        <span class="method-name">Rules</span>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="ruleProgress"></div>
                                        </div>
                                        <span class="method-score" id="ruleScore">-</span>
                                    </div>
                                    
                                    <div class="breakdown-item">
                                        <span class="method-name">Emoticons</span>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="emoticonProgress"></div>
                                        </div>
                                        <span class="method-score" id="emoticonScore">-</span>
                                    </div>
                                    
                                    <div class="breakdown-item">
                                        <span class="method-name">Punctuation</span>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="punctuationProgress"></div>
                                        </div>
                                        <span class="method-score" id="punctuationScore">-</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Long Conversation Panel -->
                    <div class="long-conversation-panel" id="longConversationPanel">
                        <div class="panel-header">
                            <h3><i class="fas fa-brain"></i> Long Conversation</h3>
                            <button class="panel-toggle" id="longConversationPanelToggle">
                                <i class="fas fa-chevron-down"></i>
                            </button>
                        </div>
                        
                        <div class="panel-content" id="longConversationPanelContent">
                            <div class="conversation-summary">
                                <h4>Conversation Summary</h4>
                                <div class="summary-stats">
                                    <div class="stat-item">
                                        <span class="stat-label">Messages</span>
                                        <span class="stat-value" id="messageCount">0</span>
                                    </div>
                                    <div class="stat-item">
                                        <span class="stat-label">Duration</span>
                                        <span class="stat-value" id="conversationDuration">0m</span>
                                    </div>
                                    <div class="stat-item">
                                        <span class="stat-label">Engagement</span>
                                        <span class="stat-value" id="engagementLevel">Low</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="topic-detection">
                                <h4>Detected Topics</h4>
                                <div class="topics-list" id="topicsList">
                                    <span class="no-topics">No topics detected yet</span>
                                </div>
                            </div>
                            
                            <div class="intelligent-suggestions">
                                <h4>Intelligent Suggestions</h4>
                                <div class="suggestions-list" id="suggestionsList">
                                    <span class="no-suggestions">Start chatting to get suggestions</span>
                                </div>
                            </div>
                            
                            <div class="conversation-insights">
                                <h4>Conversation Insights</h4>
                                <div class="insights-content" id="insightsContent">
                                    <span class="no-insights">Continue the conversation to see insights</span>
                                </div>
                            </div>
                            
                            <div class="action-buttons">
                                <button class="action-btn" id="analyzeConversationBtn">
                                    <i class="fas fa-chart-bar"></i> Analyze Conversation
                                </button>
                                <button class="action-btn" id="getSuggestionsBtn">
                                    <i class="fas fa-lightbulb"></i> Get Suggestions
                                </button>
                                <button class="action-btn" id="resetSessionBtn">
                                    <i class="fas fa-redo"></i> New Session
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>

        <script src="/static/script.js"></script>
    </body>
    </html>
    """)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "SentimentBot Pro is running successfully with full sentiment analysis",
        "deployment": "successful",
        "endpoints": ["/", "/health", "/chat"],
        "features": [
            "AI Sentiment Analysis",
            "Long Conversation Support", 
            "Real-time Analytics",
            "Topic Detection"
        ]
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_input = data['message'].strip()
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Perform comprehensive sentiment analysis
        sentiment_results = analyze_sentiment_comprehensive(user_input)
        
        # Generate contextual response
        response = generate_contextual_response(sentiment_results, user_input)
        
        return jsonify({
            'user_message': user_input,
            'bot_response': response,
            'sentiment_analysis': sentiment_results,
            'timestamp': datetime.now().strftime("%I:%M %p"),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/test')
def test():
    return jsonify({
        "message": "Test endpoint working perfectly!",
        "timestamp": "deployment successful",
        "status": "success",
        "vercel": "working"
    })

# Export the Flask app for Vercel
app.debug = False

# This is the WSGI application that Vercel will use
