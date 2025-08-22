from flask import Flask, request, jsonify, render_template
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    analysis = TextBlob(user_input)
    sentiment = analysis.sentiment

    response = {
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity,
        'response': generate_response(sentiment.polarity)
    }
    return jsonify(response)

def generate_response(polarity):
    if polarity > 0:
        return "I'm glad to hear you're feeling positive!"
    elif polarity < 0:
        return "I'm sorry to hear that you're feeling down."
    else:
        return "It seems you're neutral about this."

if __name__ == '__main__':
    app.run(debug=True)