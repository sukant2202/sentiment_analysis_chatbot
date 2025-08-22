#!/usr/bin/env python3
"""
Test script for SentimentBot - AI-Powered Sentiment Analysis Chatbot
This script tests the sentiment analysis functionality without running the web server.
"""

import sys
import os

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_sentiment_analysis():
    """Test the sentiment analysis functionality"""
    print("🧪 Testing SentimentBot Sentiment Analysis")
    print("=" * 50)
    
    try:
        # Import the sentiment analysis functions
        from app import analyze_sentiment_comprehensive, generate_contextual_response
        
        # Test messages with different sentiments
        test_messages = [
            {
                "message": "I'm feeling absolutely amazing today! Everything is going perfectly! 😊",
                "expected": "positive",
                "description": "Very positive message with emoji"
            },
            {
                "message": "I love this new restaurant! The food is incredible and the service is outstanding!",
                "expected": "positive",
                "description": "Positive message about restaurant"
            },
            {
                "message": "I'm having such a terrible day. Nothing is working out for me.",
                "expected": "negative",
                "description": "Negative message about bad day"
            },
            {
                "message": "I hate this job so much. I'm so frustrated and angry all the time.",
                "expected": "negative",
                "description": "Very negative message about job"
            },
            {
                "message": "The weather is okay, I guess. Not too bad, not too good.",
                "expected": "neutral",
                "description": "Neutral message about weather"
            },
            {
                "message": "I'm just checking in to see how things are going.",
                "expected": "neutral",
                "description": "Neutral check-in message"
            },
            {
                "message": "How are you doing today?",
                "expected": "neutral",
                "description": "Greeting question"
            },
            {
                "message": "This is absolutely fantastic! I can't believe how wonderful everything is! 🌟✨",
                "expected": "positive",
                "description": "Extremely positive with multiple exclamations and emojis"
            },
            {
                "message": "I'm devastated and heartbroken. This is the worst thing that could happen.",
                "expected": "negative",
                "description": "Very negative emotional message"
            }
        ]
        
        print(f"Testing {len(test_messages)} different message types...")
        print()
        
        correct_predictions = 0
        total_messages = len(test_messages)
        
        for i, test_case in enumerate(test_messages, 1):
            message = test_case["message"]
            expected = test_case["expected"]
            description = test_case["description"]
            
            print(f"Test {i}: {description}")
            print(f"Message: \"{message}\"")
            print(f"Expected: {expected}")
            
            try:
                # Analyze sentiment
                sentiment_results = analyze_sentiment_comprehensive(message)
                actual = sentiment_results['final_sentiment']
                confidence = sentiment_results['confidence']
                combined_score = sentiment_results['combined_score']
                
                print(f"Actual: {actual}")
                print(f"Confidence: {confidence:.3f}")
                print(f"Combined Score: {combined_score:.3f}")
                
                # Check if prediction is correct
                if actual == expected:
                    print("✅ CORRECT")
                    correct_predictions += 1
                else:
                    print("❌ INCORRECT")
                
                # Show detailed breakdown
                print(f"  TextBlob: {sentiment_results['textblob']['polarity']:.3f}")
                print(f"  VADER: {sentiment_results['vader']['compound']:.3f}")
                print(f"  Keywords: {sentiment_results['keyword_based']:.3f}")
                print(f"  Rules: {sentiment_results['rule_based']:.3f}")
                
                # Test response generation
                response = generate_contextual_response(sentiment_results, message)
                print(f"  Bot Response: {response}")
                
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
            
            print("-" * 50)
            print()
        
        # Print summary
        accuracy = (correct_predictions / total_messages) * 100
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total_messages}")
        print(f"Correct Predictions: {correct_predictions}")
        print(f"Accuracy: {accuracy:.1f}%")
        
        if accuracy >= 80:
            print("🎉 Excellent! Sentiment analysis is working well!")
        elif accuracy >= 60:
            print("👍 Good! Sentiment analysis is mostly accurate.")
        else:
            print("⚠️  Sentiment analysis needs improvement.")
        
        return accuracy >= 60
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("Make sure you have installed all dependencies and NLTK data.")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

def test_individual_components():
    """Test individual sentiment analysis components"""
    print("🔧 Testing Individual Components")
    print("=" * 50)
    
    try:
        from app import analyze_keywords, rule_based_sentiment
        
        # Test keyword analysis
        print("Testing Keyword Analysis:")
        test_texts = [
            "I love this amazing wonderful fantastic experience",
            "I hate this terrible awful horrible situation",
            "The weather is normal and regular today"
        ]
        
        for text in test_texts:
            score = analyze_keywords(text)
            print(f"  '{text}' -> Score: {score:.3f}")
        
        print()
        
        # Test rule-based analysis
        print("Testing Rule-based Analysis:")
        test_texts = [
            "This is great!!!",
            "I'm sad :(",
            "WHY IS THIS HAPPENING?",
            "Everything is fine :)"
        ]
        
        for text in test_texts:
            score = rule_based_sentiment(text)
            print(f"  '{text}' -> Score: {score:.3f}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Component Test Error: {str(e)}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("⚙️  Testing Configuration")
    print("=" * 50)
    
    try:
        from config import Config
        
        print(f"TextBlob Weight: {Config.TEXTBLOB_WEIGHT}")
        print(f"VADER Weight: {Config.VADER_WEIGHT}")
        print(f"Keyword Weight: {Config.KEYWORD_WEIGHT}")
        print(f"Rule-based Weight: {Config.RULE_BASED_WEIGHT}")
        print(f"Confidence Threshold: {Config.SENTIMENT_CONFIDENCE_THRESHOLD}")
        print(f"Positive Words Count: {len(Config.POSITIVE_WORDS)}")
        print(f"Negative Words Count: {len(Config.NEGATIVE_WORDS)}")
        print(f"Response Templates: {len(Config.RESPONSE_TEMPLATES)} categories")
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🤖 SentimentBot Component Testing")
    print("=" * 60)
    print()
    
    # Test configuration
    config_ok = test_configuration()
    print()
    
    # Test individual components
    components_ok = test_individual_components()
    print()
    
    # Test full sentiment analysis
    sentiment_ok = test_sentiment_analysis()
    print()
    
    # Overall result
    print("🎯 OVERALL TEST RESULTS")
    print("=" * 60)
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Components: {'✅ PASS' if components_ok else '❌ FAIL'}")
    print(f"Sentiment Analysis: {'✅ PASS' if sentiment_ok else '❌ FAIL'}")
    
    if all([config_ok, components_ok, sentiment_ok]):
        print("\n🎉 All tests passed! SentimentBot is ready to use.")
        print("Run 'python app.py' to start the web application.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed and NLTK data is downloaded.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
