// SentimentBot - Enhanced JavaScript Functionality
class SentimentBot {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupPanelToggle();
        this.updateStatus('Ready');
    }

    initializeElements() {
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.sentimentPanel = document.getElementById('sentimentPanel');
        this.panelContent = document.getElementById('panelContent');
        this.panelToggle = document.getElementById('panelToggle');
        
        // Sentiment visualization elements
        this.scoreCircle = document.getElementById('scoreCircle');
        this.scoreText = document.getElementById('scoreText');
        this.sentimentLabel = document.getElementById('sentimentLabel');
        this.confidenceLabel = document.getElementById('confidenceLabel');
        
        // Progress bars
        this.textblobProgress = document.getElementById('textblobProgress');
        this.vaderProgress = document.getElementById('vaderProgress');
        this.keywordProgress = document.getElementById('keywordProgress');
        this.ruleProgress = document.getElementById('ruleProgress');
        
        // Scores
        this.textblobScore = document.getElementById('textblobScore');
        this.vaderScore = document.getElementById('vaderScore');
        this.keywordScore = document.getElementById('keywordScore');
        this.ruleScore = document.getElementById('ruleScore');
    }

    bindEvents() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Auto-resize input
        this.userInput.addEventListener('input', () => {
            this.userInput.style.height = 'auto';
            this.userInput.style.height = this.userInput.scrollHeight + 'px';
        });
    }

    setupPanelToggle() {
        this.panelToggle.addEventListener('click', () => {
            const isExpanded = this.panelContent.style.display !== 'none';
            this.panelContent.style.display = isExpanded ? 'none' : 'block';
            this.panelToggle.innerHTML = isExpanded ? 
                '<i class="fas fa-chevron-down"></i>' : 
                '<i class="fas fa-chevron-up"></i>';
        });
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;

        // Clear input and add loading state
        this.userInput.value = '';
        this.setLoadingState(true);
        this.updateStatus('Analyzing...');

        // Add user message to chat
        this.addMessage(message, 'user');

        try {
            const response = await this.analyzeSentiment(message);
            this.handleResponse(response);
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('Sorry, I encountered an error while analyzing your message. Please try again.', 'bot');
            this.updateStatus('Error');
        } finally {
            this.setLoadingState(false);
            this.updateStatus('Ready');
        }
    }

    async analyzeSentiment(message) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    handleResponse(response) {
        // Add bot response to chat
        this.addMessage(response.bot_response, 'bot');
        
        // Update sentiment visualization
        this.updateSentimentVisualization(response.sentiment_analysis);
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${this.escapeHtml(content)}</p>
                    <div class="message-timestamp">${timestamp}</div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="bot-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>${this.escapeHtml(content)}</p>
                    <div class="message-timestamp">${timestamp}</div>
                </div>
            `;
        }
        
        this.chatMessages.appendChild(messageDiv);
    }

    updateSentimentVisualization(sentimentData) {
        // Update main sentiment display
        const sentiment = sentimentData.final_sentiment;
        const confidence = sentimentData.confidence;
        const combinedScore = sentimentData.combined_score;
        
        // Update score circle
        this.scoreCircle.className = `score-circle ${sentiment}`;
        this.scoreText.textContent = (combinedScore * 100).toFixed(0);
        
        // Update labels
        this.sentimentLabel.textContent = this.capitalizeFirst(sentiment);
        this.confidenceLabel.textContent = this.getConfidenceLevel(confidence);
        
        // Update progress bars with animation
        this.animateProgressBar(this.textblobProgress, sentimentData.textblob.polarity);
        this.animateProgressBar(this.vaderProgress, sentimentData.vader.compound);
        this.animateProgressBar(this.keywordProgress, sentimentData.keyword_based);
        this.animateProgressBar(this.ruleProgress, sentimentData.rule_based);
        
        // Update score displays
        this.textblobScore.textContent = sentimentData.textblob.polarity.toFixed(2);
        this.vaderScore.textContent = sentimentData.vader.compound.toFixed(2);
        this.keywordScore.textContent = sentimentData.keyword_based.toFixed(2);
        this.ruleScore.textContent = sentimentData.rule_based.toFixed(2);
        
        // Add visual feedback
        this.addSentimentFeedback(sentiment);
    }

    animateProgressBar(progressBar, value) {
        // Convert value from -1 to 1 range to 0 to 100 range
        const percentage = ((value + 1) / 2) * 100;
        
        // Reset and animate
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.width = `${percentage}%`;
        }, 100);
    }

    addSentimentFeedback(sentiment) {
        // Add visual feedback based on sentiment
        const feedbackClass = `sentiment-${sentiment}`;
        
        // Remove existing feedback classes
        this.sentimentPanel.classList.remove('sentiment-positive', 'sentiment-negative', 'sentiment-neutral');
        
        // Add new feedback class
        this.sentimentPanel.classList.add(feedbackClass);
        
        // Add subtle animation
        this.sentimentPanel.style.transform = 'scale(1.02)';
        setTimeout(() => {
            this.sentimentPanel.style.transform = 'scale(1)';
        }, 200);
    }

    getConfidenceLevel(confidence) {
        if (confidence > 0.7) return 'High Confidence';
        if (confidence > 0.4) return 'Medium Confidence';
        return 'Low Confidence';
    }

    capitalizeFirst(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    setLoadingState(loading) {
        if (loading) {
            this.sendButton.classList.add('loading');
            this.userInput.disabled = true;
        } else {
            this.sendButton.classList.remove('loading');
            this.userInput.disabled = false;
        }
    }

    updateStatus(status) {
        const statusText = this.statusIndicator.querySelector('.status-text');
        const statusDot = this.statusIndicator.querySelector('.status-dot');
        
        statusText.textContent = status;
        
        // Update status dot color based on status
        statusDot.className = 'status-dot';
        if (status === 'Ready') {
            statusDot.style.background = '#10b981';
        } else if (status === 'Analyzing...') {
            statusDot.style.background = '#f59e0b';
        } else if (status === 'Error') {
            statusDot.style.background = '#ef4444';
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    // Utility method to test sentiment analysis
    async testSentimentAnalysis() {
        const testMessages = [
            "I'm feeling absolutely amazing today! Everything is going perfectly! 😊",
            "I'm having such a terrible day. Nothing is working out for me.",
            "The weather is okay, I guess. Not too bad, not too good.",
            "I love this new restaurant! The food is incredible and the service is outstanding!",
            "I hate this job so much. I'm so frustrated and angry all the time."
        ];

        console.log('Testing sentiment analysis with sample messages...');
        
        for (const message of testMessages) {
            try {
                const response = await this.analyzeSentiment(message);
                console.log(`Message: "${message}"`);
                console.log(`Sentiment: ${response.sentiment_analysis.final_sentiment}`);
                console.log(`Confidence: ${response.sentiment_analysis.confidence}`);
                console.log('---');
            } catch (error) {
                console.error(`Error testing message: ${message}`, error);
            }
        }
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.sentimentBot = new SentimentBot();
    
    // Add some helpful tips
    console.log('SentimentBot initialized! Try saying:');
    console.log('- "I\'m feeling great today!"');
    console.log('- "I\'m having a bad day"');
    console.log('- "How are you?"');
    console.log('- "The weather is nice"');
    
    // Uncomment the line below to test sentiment analysis with sample messages
    // window.sentimentBot.testSentimentAnalysis();
});

// Add some additional utility functions
window.SentimentBotUtils = {
    // Function to manually analyze text without sending to chat
    async analyzeTextOnly(text) {
        try {
            const response = await fetch('/sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error analyzing text:', error);
            throw error;
        }
    },
    
    // Function to get system health
    async getSystemHealth() {
        try {
            const response = await fetch('/health');
            return await response.json();
        } catch (error) {
            console.error('Error getting system health:', error);
            throw error;
        }
    }
};
