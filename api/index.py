from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

# Create a standalone Flask app for Vercel
app = Flask(__name__)
CORS(app)

# Set NLTK data path for Vercel
os.environ['NLTK_DATA_PATH'] = '/tmp/nltk_data'

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SentimentBot Pro - Deployed! 🎉</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; }
            .status { color: #4ade80; font-weight: bold; font-size: 1.5em; margin: 20px 0; }
            .feature { margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px; }
            .emoji { font-size: 3em; margin: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 SentimentBot Pro</h1>
            <p class="status">✅ Successfully Deployed on Vercel!</p>
            
            <div class="feature">
                <div class="emoji">🧠</div>
                <h3>AI-Powered Sentiment Analysis</h3>
                <p>Advanced chatbot with real-time sentiment analysis</p>
            </div>
            
            <div class="feature">
                <div class="emoji">💬</div>
                <h3>Long Conversation Support</h3>
                <p>Intelligent topic detection and contextual responses</p>
            </div>
            
            <div class="feature">
                <div class="emoji">📊</div>
                <h3>Real-time Analytics</h3>
                <p>Live sentiment scoring with confidence levels</p>
            </div>
            
            <p><strong>Status:</strong> Application is running successfully on Vercel!</p>
        </div>
    </body>
    </html>
    """)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "SentimentBot Pro is running on Vercel",
        "deployment": "successful"
    })

@app.route('/test')
def test():
    return jsonify({
        "message": "Test endpoint working!",
        "timestamp": "now",
        "status": "success"
    })

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({
        "message": "Chat endpoint is working! This is a simplified version for Vercel deployment.",
        "status": "success"
    })

# Export the Flask app for Vercel
app.debug = False
