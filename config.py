# SentimentBot Pro - Advanced Configuration
import os

class Config:
    """Configuration class for the SentimentBot Pro - AI-Powered Sentiment Analysis & Long Conversation Chatbot"""
    
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
    
    # Long Conversation Configuration
    MAX_CONVERSATION_MEMORY = int(os.environ.get('MAX_CONVERSATION_MEMORY', 50))
    SESSION_TIMEOUT_MINUTES = int(os.environ.get('SESSION_TIMEOUT_MINUTES', 60))
    MIN_MESSAGES_FOR_INSIGHTS = int(os.environ.get('MIN_MESSAGES_FOR_INSIGHTS', 5))
    MIN_MESSAGES_FOR_SUGGESTIONS = int(os.environ.get('MIN_MESSAGES_FOR_SUGGESTIONS', 3))
    
    # Topic Detection Configuration
    TOPIC_DETECTION_CONFIDENCE = float(os.environ.get('TOPIC_DETECTION_CONFIDENCE', 0.6))
    MAX_TOPICS_PER_MESSAGE = int(os.environ.get('MAX_TOPICS_PER_MESSAGE', 3))
    
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
        'fortunate', 'lucky', 'successful', 'achievement', 'victory', 'triumph',
        'inspiring', 'motivating', 'empowering', 'fulfilling', 'rewarding', 'valuable'
    }
    
    NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike',
        'sad', 'angry', 'frustrated', 'disappointed', 'upset', 'worried', 'anxious',
        'depressed', 'miserable', 'painful', 'suffering', 'terrible', 'dreadful',
        'devastated', 'heartbroken', 'crushed', 'defeated', 'hopeless', 'desperate',
        'furious', 'enraged', 'irritated', 'annoyed', 'bothered', 'troubled',
        'overwhelmed', 'stressed', 'exhausted', 'burned_out', 'isolated', 'lonely'
    }
    
    # Emoticons for Rule-based Analysis
    POSITIVE_EMOTICONS = [
        ':)', ':-)', '😊', '😄', '😃', '😀', '😁', '😆', '😅', '🤗',
        '😍', '🥰', '😘', '😋', '😎', '🤩', '🥳', '😇', '🤠', '👻',
        '👍', '👏', '🎉', '🎊', '✨', '🌟', '💫', '🔥', '💯', '🏆'
    ]
    
    NEGATIVE_EMOTICONS = [
        ':(', ':-(', '😢', '😭', '😞', '😔', '😟', '😕', '😣', '😖',
        '😡', '😠', '😤', '😾', '😿', '💔', '😰', '😨', '😧', '😦',
        '👎', '😤', '😩', '😫', '😵', '🤢', '🤮', '💀', '☠️', '💩'
    ]
    
    # Topic Detection Keywords and Categories
    TOPIC_KEYWORDS = {
        'technology': [
            'computer', 'software', 'programming', 'ai', 'machine learning', 'data', 
            'internet', 'app', 'digital', 'tech', 'code', 'algorithm', 'database', 
            'cloud', 'cybersecurity', 'blockchain', 'virtual reality', 'augmented reality',
            'robotics', 'automation', 'smartphone', 'gadget', 'innovation', 'startup'
        ],
        'health': [
            'health', 'medical', 'doctor', 'hospital', 'medicine', 'symptoms', 
            'treatment', 'exercise', 'diet', 'nutrition', 'fitness', 'wellness', 
            'mental health', 'therapy', 'recovery', 'prevention', 'diagnosis',
            'meditation', 'yoga', 'workout', 'gym', 'wellbeing', 'lifestyle'
        ],
        'education': [
            'school', 'university', 'college', 'study', 'learning', 'course', 
            'degree', 'student', 'teacher', 'professor', 'education', 'academic', 
            'research', 'knowledge', 'skill', 'training', 'certification',
            'online learning', 'e-learning', 'workshop', 'seminar', 'lecture'
        ],
        'work': [
            'job', 'career', 'work', 'office', 'business', 'company', 'project', 
            'meeting', 'colleague', 'boss', 'salary', 'promotion', 'workplace', 
            'professional', 'industry', 'leadership', 'management', 'teamwork',
            'deadline', 'presentation', 'client', 'customer', 'entrepreneur'
        ],
        'relationships': [
            'friend', 'family', 'partner', 'relationship', 'love', 'dating', 
            'marriage', 'parent', 'child', 'sibling', 'romance', 'connection', 
            'social', 'community', 'communication', 'trust', 'support',
            'companionship', 'intimacy', 'commitment', 'loyalty', 'understanding'
        ],
        'finance': [
            'money', 'finance', 'investment', 'banking', 'budget', 'savings', 
            'expenses', 'income', 'tax', 'insurance', 'loan', 'credit', 
            'financial', 'economy', 'market', 'stocks', 'bonds', 'retirement',
            'planning', 'debt', 'wealth', 'assets', 'liabilities'
        ],
        'travel': [
            'travel', 'vacation', 'trip', 'destination', 'hotel', 'flight', 
            'tourism', 'adventure', 'explore', 'journey', 'culture', 'experience', 
            'sightseeing', 'backpacking', 'road trip', 'cruise', 'hiking',
            'beach', 'mountains', 'city', 'country', 'international'
        ],
        'hobbies': [
            'hobby', 'interest', 'passion', 'activity', 'sport', 'music', 
            'art', 'reading', 'gaming', 'cooking', 'gardening', 'photography', 
            'crafting', 'collecting', 'outdoor', 'painting', 'drawing',
            'writing', 'dancing', 'singing', 'playing', 'creating'
        ],
        'current_events': [
            'news', 'politics', 'world', 'society', 'environment', 'climate', 
            'pandemic', 'election', 'government', 'policy', 'social issues', 
            'global', 'current affairs', 'breaking news', 'headlines',
            'international', 'national', 'local', 'community', 'activism'
        ],
        'personal_development': [
            'growth', 'self-improvement', 'goals', 'motivation', 'success', 
            'happiness', 'mindset', 'productivity', 'leadership', 'confidence', 
            'skills', 'development', 'achievement', 'potential', 'transformation',
            'mindfulness', 'self-awareness', 'emotional intelligence', 'resilience'
        ]
    }
    
    # Response Templates
    RESPONSE_TEMPLATES = {
        'positive': [
            "That's wonderful! Your positive energy is contagious. 😊",
            "I'm so glad to hear that! It sounds like things are going well for you.",
            "That's fantastic! Your enthusiasm really comes through in your message.",
            "Wonderful! I can feel your positive vibes. Keep that energy going! ✨",
            "Amazing! Your positivity is inspiring. Keep spreading that joy! 🌟",
            "That's absolutely fantastic! Your positive attitude is truly admirable.",
            "I love your enthusiasm! It's wonderful to see you feeling so good.",
            "That's incredible! Your positive energy is making me smile too! 😄"
        ],
        'negative': [
            "I'm sorry to hear that you're feeling this way. Remember, it's okay to not be okay.",
            "I can sense that you're going through a difficult time. Would you like to talk more about it?",
            "I'm here to listen. Sometimes talking about our feelings can help us feel better.",
            "I understand this is tough. Remember that difficult times are temporary, and you're not alone.",
            "I hear you, and I want you to know that your feelings are valid. You're not alone in this.",
            "I'm here to support you through this challenging time. What would be most helpful right now?",
            "It sounds like you're dealing with a lot. Remember to be kind to yourself during difficult times.",
            "I can feel the weight of what you're going through. You don't have to face this alone."
        ],
        'neutral': [
            "I see you're being quite neutral about this. Would you like to elaborate?",
            "Interesting perspective. I'd love to hear more about your thoughts on this.",
            "I'm curious to know more about how you feel. Care to share?",
            "Thanks for sharing. I'd like to understand your perspective better.",
            "That's an interesting point. Tell me more about what you think.",
            "I appreciate you sharing that. What are your deeper thoughts on this matter?",
            "That's a thoughtful observation. How do you feel this relates to your broader experiences?",
            "Interesting. I'd love to explore this topic further with you."
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
        },
        'technology': {
            'positive': "Technology is amazing, isn't it? I'm glad you're excited about it!",
            'negative': "Technology can be frustrating sometimes. What specific issues are you facing?",
            'neutral': "Technology is a big part of our lives. What aspects interest you most?"
        },
        'health': {
            'positive': "That's wonderful! Taking care of your health is so important.",
            'negative': "Health challenges can be really difficult. What support do you need right now?",
            'neutral': "Health is a complex topic. What would you like to explore about it?"
        }
    }
    
    # Long Conversation Response Patterns
    LONG_CONVERSATION_RESPONSES = {
        'early_stage': [
            "I'm really enjoying our conversation so far! What would you like to explore next?",
            "This is great! I can tell you have a lot to share. What's on your mind?",
            "I'm here to listen and learn more about you. What's something you're passionate about?"
        ],
        'mid_stage': [
            "We're really getting into some interesting topics! What aspect would you like to dive deeper into?",
            "This conversation is flowing so well! What's something you'd like to explore further?",
            "I'm learning so much about you! What else would you like to discuss?"
        ],
        'advanced_stage': [
            "We've covered so much ground! What insights have you gained from our conversation?",
            "This has been such a meaningful discussion! What would you like to reflect on?",
            "I feel like we've really connected! What's something you'd like to explore next?"
        ]
    }
    
    # Intelligent Suggestion Categories
    SUGGESTION_CATEGORIES = {
        'personal': [
            "Tell me about your biggest dream or goal",
            "What's something you're proud of accomplishing?",
            "What's a challenge you've overcome that made you stronger?",
            "What values are most important to you in life?",
            "What's something you'd like to improve about yourself?"
        ],
        'professional': [
            "What's your ideal work environment like?",
            "What skills would you like to develop in your career?",
            "What's a project you're most excited about?",
            "How do you handle workplace challenges?",
            "What's your vision for your professional future?"
        ],
        'relationships': [
            "What makes a friendship meaningful to you?",
            "How do you show love and care to others?",
            "What's a relationship lesson you've learned?",
            "How do you build trust with new people?",
            "What qualities do you value most in relationships?"
        ],
        'growth': [
            "What's something new you'd like to learn this year?",
            "How do you handle setbacks and failures?",
            "What motivates you to keep growing?",
            "What's a habit you'd like to develop?",
            "How do you measure personal success?"
        ]
    }
    
    # Conversation Flow Analysis Settings
    CONVERSATION_FLOW_SETTINGS = {
        'intense_threshold_seconds': 300,  # 5 minutes
        'sporadic_threshold_seconds': 1800,  # 30 minutes
        'engagement_levels': {
            'low': 5,
            'medium': 15,
            'high': 30,
            'very_high': 50
        }
    }
    
    # Topic Suggestion Weights
    TOPIC_SUGGESTION_WEIGHTS = {
        'current_topics': 0.4,
        'user_interests': 0.3,
        'conversation_length': 0.2,
        'sentiment_trend': 0.1
    }
