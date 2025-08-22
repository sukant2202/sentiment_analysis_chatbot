from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import os

# Create Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

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
                                        <span class="method-name">TextBlob</span>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="textblobProgress"></div>
                                        </div>
                                        <span class="method-score" id="textblobScore">-</span>
                                    </div>
                                    
                                    <div class="breakdown-item">
                                        <span class="method-name">VADER</span>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="vaderProgress"></div>
                                        </div>
                                        <span class="score-text" id="vaderScore">-</span>
                                    </div>
                                    
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
        "message": "SentimentBot Pro is running successfully on Vercel",
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

        # Simple sentiment analysis (you can enhance this)
        if any(word in user_input.lower() for word in ['happy', 'great', 'amazing', 'wonderful', 'excellent']):
            sentiment = 'positive'
            score = 0.8
        elif any(word in user_input.lower() for word in ['sad', 'terrible', 'awful', 'horrible', 'bad']):
            sentiment = 'negative'
            score = -0.7
        else:
            sentiment = 'neutral'
            score = 0.0

        # Generate response based on sentiment
        if sentiment == 'positive':
            response = "That's wonderful! Your positive energy is contagious. 😊 Tell me more about what's making you feel so great!"
        elif sentiment == 'negative':
            response = "I'm sorry to hear that you're feeling this way. Remember, it's okay to not be okay. Would you like to talk more about it?"
        else:
            response = "Interesting! I'd love to hear more about your thoughts. What's on your mind?"

        return jsonify({
            'user_message': user_input,
            'bot_response': response,
            'sentiment_analysis': {
                'sentiment': sentiment,
                'score': score,
                'confidence': abs(score)
            },
            'timestamp': 'now',
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
