# Sentiment Analysis Chatbot Configuration
import os

class Config:
    """Configuration class for the Sentiment Analysis Chatbot"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Sentiment Analysis Configuration
    SENTIMENT_CONFIDENCE_THRESHOLD = float(os.environ.get('SENTIMENT_CONFIDENCE_THRESHOLD', 0.1))
    
    # Model Weights for Combined Sentiment Analysis
    TEXTBLOB_WEIGHT = float(os.environ.get('TEXTBLOB_WEIGHT', 0.3))
    VADER_WEIGHT = float(os.environ.get('VADER_WEIGHT', 0.4))
    KEYWORD_WEIGHT = float(os.environ.get('KEYWORD_WEIGHT', 0.2))
    RULE_BASED_WEIGHT = float(os.environ.get('RULE_BASED_WEIGHT', 0.1))
    
    # NLTK Configuration
    NLTK_DATA_PATH = os.environ.get('NLTK_DATA_PATH', './nltk_data')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Sentiment Keywords
    POSITIVE_WORDS = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
        'happy', 'joy', 'love', 'like', 'enjoy', 'pleased', 'satisfied', 'perfect',
        'beautiful', 'nice', 'wonderful', 'brilliant', 'outstanding', 'superb',
        'delighted', 'ecstatic', 'thrilled', 'excited', 'grateful', 'blessed',
        'fortunate', 'lucky', 'successful', 'achievement', 'victory', 'triumph'
    }
    
    NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike',
        'sad', 'angry', 'frustrated', 'disappointed', 'upset', 'worried', 'anxious',
        'depressed', 'miserable', 'painful', 'suffering', 'terrible', 'dreadful',
        'devastated', 'heartbroken', 'crushed', 'defeated', 'hopeless', 'desperate',
        'furious', 'enraged', 'irritated', 'annoyed', 'bothered', 'troubled'
    }
    
    # Emoticons for Rule-based Analysis
    POSITIVE_EMOTICONS = [
        ':)', ':-)', '😊', '😄', '😃', '😀', '😁', '😆', '😅', '🤗',
        '😍', '🥰', '😘', '😋', '😎', '🤩', '🥳', '😇', '🤠', '👻'
    ]
    
    NEGATIVE_EMOTICONS = [
        ':(', ':-(', '😢', '😭', '😞', '😔', '😟', '😕', '😣', '😖',
        '😡', '😠', '😤', '😾', '😿', '💔', '😰', '😨', '😧', '😦'
    ]
    
    # Response Templates
    RESPONSE_TEMPLATES = {
        'positive': [
            "That's wonderful! Your positive energy is contagious. 😊",
            "I'm so glad to hear that! It sounds like things are going well for you.",
            "That's fantastic! Your enthusiasm really comes through in your message.",
            "Wonderful! I can feel your positive vibes. Keep that energy going! ✨",
            "Amazing! Your positivity is inspiring. Keep spreading that joy! 🌟"
        ],
        'negative': [
            "I'm sorry to hear that you're feeling this way. Remember, it's okay to not be okay.",
            "I can sense that you're going through a difficult time. Would you like to talk more about it?",
            "I'm here to listen. Sometimes talking about our feelings can help us feel better.",
            "I understand this is tough. Remember that difficult times are temporary, and you're not alone.",
            "I hear you, and I want you to know that your feelings are valid. You're not alone in this."
        ],
        'neutral': [
            "I see you're being quite neutral about this. Would you like to elaborate?",
            "Interesting perspective. I'd love to hear more about your thoughts on this.",
            "I'm curious to know more about how you feel. Care to share?",
            "Thanks for sharing. I'd like to understand your perspective better.",
            "That's an interesting point. Tell me more about what you think."
        ]
    }
    
    # Context-aware Response Patterns
    CONTEXT_PATTERNS = {
        'greeting': {
            'positive': "I'm doing great, and I can sense your positive energy! How can I help you today?",
            'negative': "I'm here for you. I notice you might be having a tough time. Would you like to talk about it?",
            'neutral': "I'm doing well, thank you for asking. How are you feeling today?"
        },
        'weather': {
            'positive': "The weather sounds lovely! It's amazing how good weather can lift our spirits.",
            'negative': "I understand weather can affect our mood. Is there something else on your mind?",
            'neutral': "Weather can be quite neutral sometimes. How are you feeling otherwise?"
        },
        'work': {
            'positive': "That's fantastic! It's wonderful when work brings us joy and satisfaction.",
            'negative': "Work stress can be really challenging. Would you like to talk about what's happening?",
            'neutral': "Work can be quite routine sometimes. How are you feeling about other aspects of your life?"
        }
    }
