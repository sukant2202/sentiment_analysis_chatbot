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
        this.textblobProgress = document.getElementById('textblobProgress');
        this.vaderProgress = document.getElementById('vaderProgress');
        this.keywordProgress = document.getElementById('keywordProgress');
        this.ruleProgress = document.getElementById('ruleProgress');
        
        // Scores
        this.textblobScore = document.getElementById('textblobScore');
        this.vaderScore = document.getElementById('vaderScore');
        this.keywordScore = document.getElementById('keywordScore');
        this.ruleScore = document.getElementById('ruleScore');
        
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

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
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
        this.messageCount++;

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
            body: JSON.stringify({ 
                message: message,
                session_id: this.sessionId
            }),
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
        
        // Update long conversation features
        this.updateLongConversationFeatures(response);
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    updateLongConversationFeatures(response) {
        // Update conversation summary
        this.updateConversationSummary(response.conversation_summary);
        
        // Update topic detection
        this.updateTopicDetection(response.detected_topics);
        
        // Update suggestions
        this.updateSuggestions(response.suggestions);
        
        // Update conversation duration
        this.updateConversationDuration();
    }

    updateConversationSummary(summary) {
        if (summary && typeof summary === 'object') {
            this.messageCountElement.textContent = summary.total_messages || this.messageCount;
            this.engagementLevelElement.textContent = summary.engagement_level || 'Low';
        }
    }

    updateTopicDetection(topics) {
        if (topics && topics.length > 0) {
            this.topicsList.innerHTML = '';
            topics.forEach(topic => {
                const topicTag = document.createElement('span');
                topicTag.className = `topic-tag topic-${topic}`;
                topicTag.textContent = this.formatTopicName(topic);
                this.topicsList.appendChild(topicTag);
            });
        } else if (this.topicsList.querySelector('.no-topics')) {
            // Keep the no-topics message if no topics detected
        }
    }

    formatTopicName(topic) {
        return topic.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    updateSuggestions(suggestions) {
        if (suggestions && suggestions.length > 0) {
            this.suggestionsList.innerHTML = '';
            suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.textContent = suggestion;
                suggestionItem.addEventListener('click', () => {
                    this.userInput.value = suggestion;
                    this.userInput.focus();
                });
                this.suggestionsList.appendChild(suggestionItem);
            });
        }
    }

    updateConversationDuration() {
        const duration = new Date() - this.conversationStartTime;
        const minutes = Math.floor(duration / 60000);
        const seconds = Math.floor((duration % 60000) / 1000);
        this.conversationDurationElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
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

    // Long Conversation Methods
    async analyzeConversation() {
        try {
            this.updateStatus('Analyzing...');
            
            const response = await fetch('/long_conversation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ session_id: this.sessionId }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.displayConversationAnalysis(data);
            
        } catch (error) {
            console.error('Error analyzing conversation:', error);
            this.addMessage('Sorry, I encountered an error while analyzing our conversation. Please try again.', 'bot');
        } finally {
            this.updateStatus('Ready');
        }
    }

    displayConversationAnalysis(data) {
        // Display conversation analysis
        if (data.conversation_analysis) {
            const analysis = data.conversation_analysis;
            
            // Update summary stats
            this.messageCountElement.textContent = analysis.total_messages;
            this.engagementLevelElement.textContent = analysis.user_engagement;
            
            // Display insights
            this.displayInsights(data.insights);
            
            // Display comprehensive suggestions
            this.displayComprehensiveSuggestions(data.suggestions);
        }
    }

    displayInsights(insights) {
        if (!insights) return;
        
        this.insightsContent.innerHTML = '';
        
        // Display strengths
        if (insights.strengths && insights.strengths.length > 0) {
            insights.strengths.forEach(strength => {
                const insightItem = document.createElement('div');
                insightItem.className = 'insight-item';
                insightItem.textContent = strength;
                this.insightsContent.appendChild(insightItem);
            });
        }
        
        // Display areas for growth
        if (insights.areas_for_growth && insights.areas_for_growth.length > 0) {
            insights.areas_for_growth.forEach(area => {
                const insightItem = document.createElement('div');
                insightItem.className = 'insight-item warning';
                insightItem.textContent = area;
                this.insightsContent.appendChild(insightItem);
            });
        }
        
        // Display recommendations
        if (insights.recommendations && insights.recommendations.length > 0) {
            insights.recommendations.forEach(recommendation => {
                const insightItem = document.createElement('div');
                insightItem.className = 'insight-item info';
                insightItem.textContent = recommendation;
                this.insightsContent.appendChild(insightItem);
            });
        }
        
        if (this.insightsContent.children.length === 0) {
            this.insightsContent.innerHTML = '<div class="no-insights">Continue the conversation to see insights</div>';
        }
    }

    displayComprehensiveSuggestions(suggestions) {
        if (!suggestions) return;
        
        this.suggestionsList.innerHTML = '';
        
        // Display immediate suggestions
        if (suggestions.immediate && suggestions.immediate.length > 0) {
            suggestions.immediate.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.textContent = `💡 ${suggestion}`;
                suggestionItem.addEventListener('click', () => {
                    this.userInput.value = suggestion;
                    this.userInput.focus();
                });
                this.suggestionsList.appendChild(suggestionItem);
            });
        }
        
        // Display short-term suggestions
        if (suggestions.short_term && suggestions.short_term.length > 0) {
            suggestions.short_term.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.textContent = `📅 ${suggestion}`;
                this.suggestionsList.appendChild(suggestionItem);
            });
        }
        
        // Display long-term suggestions
        if (suggestions.long_term && suggestions.long_term.length > 0) {
            suggestions.long_term.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.textContent = `🎯 ${suggestion}`;
                this.suggestionsList.appendChild(suggestionItem);
            });
        }
        
        if (this.suggestionsList.children.length === 0) {
            this.suggestionsList.innerHTML = '<div class="no-suggestions">Start chatting to get personalized suggestions</div>';
        }
    }

    async getSuggestions() {
        try {
            this.updateStatus('Generating suggestions...');
            
            // Trigger conversation analysis to get fresh suggestions
            await this.analyzeConversation();
            
        } catch (error) {
            console.error('Error getting suggestions:', error);
            this.addMessage('Sorry, I encountered an error while generating suggestions. Please try again.', 'bot');
        } finally {
            this.updateStatus('Ready');
        }
    }

    resetSession() {
        if (confirm('Are you sure you want to start a new conversation session? This will clear all current conversation data.')) {
            // Generate new session ID
            this.sessionId = this.generateSessionId();
            this.conversationStartTime = new Date();
            this.messageCount = 0;
            
            // Clear chat messages
            this.chatMessages.innerHTML = `
                <div class="welcome-message">
                    <div class="bot-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <p>Hello! I'm SentimentBot Pro, your AI companion with advanced sentiment analysis and long conversation capabilities. I can understand how you're feeling, track our conversation topics, and provide intelligent suggestions to keep our discussions engaging and meaningful. How are you today?</p>
                        <div class="message-timestamp">Just now</div>
                    </div>
                </div>
            `;
            
            // Reset conversation features
            this.messageCountElement.textContent = '0';
            this.conversationDurationElement.textContent = '0:00';
            this.engagementLevelElement.textContent = 'Low';
            this.topicsList.innerHTML = '<div class="no-topics">No topics detected yet</div>';
            this.suggestionsList.innerHTML = '<div class="no-suggestions">Start chatting to get personalized suggestions</div>';
            this.insightsContent.innerHTML = '<div class="no-insights">Continue the conversation to see insights</div>';
            
            // Reset sentiment visualization
            this.scoreCircle.className = 'score-circle neutral';
            this.scoreText.textContent = '-';
            this.sentimentLabel.textContent = 'Neutral';
            this.confidenceLabel.textContent = '-';
            
            this.addMessage('New conversation session started! I\'m ready to help you with a fresh perspective.', 'bot');
        }
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
    window.sentimentBot = new SentimentBotPro();
    
    // Add some helpful tips
    console.log('SentimentBot Pro initialized! Try saying:');
    console.log('- "I\'m feeling great today!"');
    console.log('- "I\'m having a bad day"');
    console.log('- "How are you?"');
    console.log('- "Let\'s talk about technology and AI"');
    console.log('- "I want to discuss my career goals"');
    
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
    },
    
    // Function to get conversation summary
    async getConversationSummary(sessionId) {
        try {
            const response = await fetch(`/conversation_summary/${sessionId}`);
            return await response.json();
        } catch (error) {
            console.error('Error getting conversation summary:', error);
            throw error;
        }
    }
};
