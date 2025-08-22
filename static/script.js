// SentimentBot Pro - Enhanced JavaScript Functionality with Long Conversation Support
class SentimentBotPro {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupPanelToggles();
        this.updateStatus('Ready');
        this.sessionId = this.generateSessionId();
        this.conversationStartTime = new Date();
        this.messageCount = 0;
    }

    initializeElements() {
        // Chat elements
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.statusIndicator = document.getElementById('statusIndicator');
        
        // Sentiment panel elements
        this.sentimentPanel = document.getElementById('sentimentPanel');
        this.sentimentPanelContent = document.getElementById('sentimentPanelContent');
        this.sentimentPanelToggle = document.getElementById('sentimentPanelToggle');
        
        // Long conversation panel elements
        this.longConversationPanel = document.getElementById('longConversationPanel');
        this.longConversationPanelContent = document.getElementById('longConversationPanelContent');
        this.longConversationPanelToggle = document.getElementById('longConversationPanelToggle');
        
        // Sentiment visualization elements
        this.scoreCircle = document.getElementById('scoreCircle');
        this.scoreText = document.getElementById('scoreText');
        this.sentimentLabel = document.getElementById('sentimentLabel');
        this.confidenceLabel = document.getElementById('confidenceLabel');
        
        // Progress bars
        this.keywordProgress = document.getElementById('keywordProgress');
        this.ruleProgress = document.getElementById('ruleProgress');
        this.emoticonProgress = document.getElementById('emoticonProgress');
        this.punctuationProgress = document.getElementById('punctuationProgress');
        
        // Scores
        this.keywordScore = document.getElementById('keywordScore');
        this.ruleScore = document.getElementById('ruleScore');
        this.emoticonScore = document.getElementById('emoticonScore');
        this.punctuationScore = document.getElementById('punctuationScore');
        
        // Long conversation elements
        this.messageCountElement = document.getElementById('messageCount');
        this.conversationDurationElement = document.getElementById('conversationDuration');
        this.engagementLevelElement = document.getElementById('engagementLevel');
        this.topicsList = document.getElementById('topicsList');
        this.suggestionsList = document.getElementById('suggestionsList');
        this.insightsContent = document.getElementById('insightsContent');
        
        // Action buttons
        this.analyzeConversationBtn = document.getElementById('analyzeConversationBtn');
        this.getSuggestionsBtn = document.getElementById('getSuggestionsBtn');
        this.resetSessionBtn = document.getElementById('resetSessionBtn');
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
        
        // Action button events
        this.analyzeConversationBtn.addEventListener('click', () => this.analyzeConversation());
        this.getSuggestionsBtn.addEventListener('click', () => this.getSuggestions());
        this.resetSessionBtn.addEventListener('click', () => this.resetSession());
    }

    setupPanelToggles() {
        // Sentiment panel toggle
        this.sentimentPanelToggle.addEventListener('click', () => {
            const isExpanded = this.sentimentPanelContent.style.display !== 'none';
            this.sentimentPanelContent.style.display = isExpanded ? 'none' : 'block';
            this.sentimentPanelToggle.innerHTML = isExpanded ? 
                '<i class="fas fa-chevron-down"></i>' : 
                '<i class="fas fa-chevron-up"></i>';
        });
        
        // Long conversation panel toggle
        this.longConversationPanelToggle.addEventListener('click', () => {
            const isExpanded = this.longConversationPanelContent.style.display !== 'none';
            this.longConversationPanelContent.style.display = isExpanded ? 'none' : 'block';
            this.longConversationPanelToggle.innerHTML = isExpanded ? 
                '<i class="fas fa-chevron-down"></i>' : 
                '<i class="fas fa-chevron-up"></i>';
        });
    }

    updateStatus(status) {
        const statusText = this.statusIndicator.querySelector('.status-text');
        const statusDot = this.statusIndicator.querySelector('.status-dot');
        
        statusText.textContent = status;
        
        // Update status dot color
        statusDot.className = 'status-dot';
        if (status === 'Ready') {
            statusDot.classList.add('ready');
        } else if (status === 'Typing...') {
            statusDot.classList.add('typing');
        } else if (status === 'Error') {
            statusDot.classList.add('error');
        }
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessageToChat(message, 'user');
        this.userInput.value = '';
        this.userInput.style.height = 'auto';

        // Update status
        this.updateStatus('Typing...');
        this.messageCount++;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                // Add bot response to chat
                this.addMessageToChat(data.bot_response, 'bot');
                
                // Update sentiment analysis
                this.updateSentimentAnalysis(data.sentiment_analysis);
                
                // Update conversation stats
                this.updateConversationStats();
                
                this.updateStatus('Ready');
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            this.addMessageToChat('Sorry, I encountered an error while analyzing your message. Please try again.', 'bot');
            this.updateStatus('Error');
        }
    }

    addMessageToChat(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${message}</p>
                    <div class="message-timestamp">${timestamp}</div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="bot-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>${message}</p>
                    <div class="message-timestamp">${timestamp}</div>
                </div>
            `;
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    updateSentimentAnalysis(sentimentData) {
        // Update main sentiment display
        this.scoreText.textContent = sentimentData.combined_score;
        this.sentimentLabel.textContent = sentimentData.final_sentiment;
        this.confidenceLabel.textContent = `Confidence: ${sentimentData.confidence}`;
        
        // Update progress bars and scores
        this.updateProgressBar(this.keywordProgress, this.keywordScore, sentimentData.keyword_based);
        this.updateProgressBar(this.ruleProgress, this.ruleScore, sentimentData.rule_based);
        this.updateProgressBar(this.emoticonProgress, this.emoticonScore, sentimentData.emoticon_based);
        this.updateProgressBar(this.punctuationProgress, this.punctuationScore, sentimentData.punctuation_based);
        
        // Update sentiment label color
        this.updateSentimentLabelColor(sentimentData.final_sentiment);
    }

    updateProgressBar(progressElement, scoreElement, score) {
        if (progressElement && scoreElement) {
            const percentage = Math.abs(score) * 100;
            progressElement.style.width = `${percentage}%`;
            scoreElement.textContent = score.toFixed(3);
            
            // Update progress bar color based on sentiment
            progressElement.className = 'progress-fill';
            if (score > 0) {
                progressElement.classList.add('positive');
            } else if (score < 0) {
                progressElement.classList.add('negative');
            } else {
                progressElement.classList.add('neutral');
            }
        }
    }

    updateSentimentLabelColor(sentiment) {
        this.sentimentLabel.className = 'sentiment-label';
        this.sentimentLabel.classList.add(sentiment);
    }

    updateConversationStats() {
        this.messageCountElement.textContent = this.messageCount;
        
        const duration = Math.floor((new Date() - this.conversationStartTime) / 60000);
        this.conversationDurationElement.textContent = `${duration}m`;
        
        // Update engagement level
        if (this.messageCount < 5) {
            this.engagementLevelElement.textContent = 'Low';
        } else if (this.messageCount < 15) {
            this.engagementLevelElement.textContent = 'Medium';
        } else {
            this.engagementLevelElement.textContent = 'High';
        }
    }

    analyzeConversation() {
        // Implement conversation analysis logic
        this.insightsContent.innerHTML = `
            <div class="insight-item">
                <i class="fas fa-chart-line"></i>
                <span>Conversation is ${this.messageCount > 10 ? 'very engaging' : 'developing'}</span>
            </div>
            <div class="insight-item">
                <i class="fas fa-clock"></i>
                <span>Duration: ${this.conversationDurationElement.textContent}</span>
            </div>
        `;
    }

    getSuggestions() {
        const suggestions = [
            "Try asking about your day or feelings",
            "Share something that made you happy or sad",
            "Discuss your interests or hobbies",
            "Ask for advice or support"
        ];
        
        this.suggestionsList.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-item">${suggestion}</div>`
        ).join('');
    }

    resetSession() {
        this.messageCount = 0;
        this.conversationStartTime = new Date();
        this.sessionId = this.generateSessionId();
        
        // Clear chat messages except welcome message
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        this.chatMessages.innerHTML = '';
        if (welcomeMessage) {
            this.chatMessages.appendChild(welcomeMessage);
        }
        
        // Reset sentiment analysis
        this.scoreText.textContent = '-';
        this.sentimentLabel.textContent = 'Neutral';
        this.confidenceLabel.textContent = '-';
        
        // Reset progress bars
        [this.keywordProgress, this.ruleProgress, this.emoticonProgress, this.punctuationProgress].forEach(progress => {
            if (progress) {
                progress.style.width = '0%';
                progress.className = 'progress-fill';
            }
        });
        
        // Reset scores
        [this.keywordScore, this.ruleScore, this.emoticonScore, this.punctuationScore].forEach(score => {
            if (score) score.textContent = '-';
        });
        
        // Reset conversation stats
        this.updateConversationStats();
        
        this.updateStatus('Ready');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SentimentBotPro();
});
