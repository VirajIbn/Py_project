// Chat Application JavaScript
class ChatApp {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.clearButton = document.getElementById('clearButton');
        this.copyButton = document.getElementById('copyButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.charCount = document.getElementById('charCount');
        this.errorModal = document.getElementById('errorModal');
        this.errorMessage = document.getElementById('errorMessage');
        this.modalOk = document.getElementById('modalOk');
        this.closeModal = document.getElementById('closeModal');
        
        this.isTyping = false;
        this.lastBotMessage = '';
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateCurrentTime();
        this.setStatus('ready', 'Ready');
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.autoResizeTextarea();
            this.updateCharCount();
            this.toggleSendButton();
        });
        
        // Update time every minute
        setInterval(() => this.updateCurrentTime(), 60000);
    }
    
    setupEventListeners() {
        // Send message events
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Action buttons
        this.clearButton.addEventListener('click', () => this.clearChat());
        this.copyButton.addEventListener('click', () => this.copyLastResponse());
        
        // Modal events
        this.modalOk.addEventListener('click', () => this.hideErrorModal());
        this.closeModal.addEventListener('click', () => this.hideErrorModal());
        this.errorModal.addEventListener('click', (e) => {
            if (e.target === this.errorModal) {
                this.hideErrorModal();
            }
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        this.updateCharCount();
        this.toggleSendButton();
        
        // Show typing indicator
        this.showTypingIndicator();
        this.setStatus('typing', 'AI is typing...');
        
        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            if (data.success) {
                // Add bot response to chat
                this.addMessage(data.response, 'bot');
                this.lastBotMessage = data.response;
                this.setStatus('ready', 'Ready');
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            this.setStatus('error', 'Connection Error');
            this.showErrorModal('Failed to get response from AI. Please try again.');
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.typingIndicator.classList.add('show');
        this.isTyping = true;
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.classList.remove('show');
        this.isTyping = false;
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear all messages?')) {
            // Keep only the initial bot message
            const initialMessage = this.chatMessages.querySelector('.bot-message');
            this.chatMessages.innerHTML = '';
            if (initialMessage) {
                this.chatMessages.appendChild(initialMessage);
            }
            this.lastBotMessage = '';
            this.setStatus('ready', 'Chat cleared');
        }
    }
    
    copyLastResponse() {
        if (this.lastBotMessage) {
            navigator.clipboard.writeText(this.lastBotMessage).then(() => {
                this.showToast('Response copied to clipboard!');
            }).catch(() => {
                this.showToast('Failed to copy to clipboard');
            });
        } else {
            this.showToast('No response to copy');
        }
    }
    
    showErrorModal(message) {
        this.errorMessage.textContent = message;
        this.errorModal.classList.add('show');
    }
    
    hideErrorModal() {
        this.errorModal.classList.remove('show');
    }
    
    setStatus(status, text) {
        this.statusText.textContent = text;
        this.statusDot.className = 'status-dot';
        
        switch (status) {
            case 'ready':
                this.statusDot.style.background = '#4CAF50';
                break;
            case 'typing':
                this.statusDot.style.background = '#FF9800';
                break;
            case 'error':
                this.statusDot.style.background = '#f44336';
                break;
            default:
                this.statusDot.style.background = '#666';
        }
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/1000`;
        
        if (count > 900) {
            this.charCount.style.color = '#f44336';
        } else if (count > 700) {
            this.charCount.style.color = '#FF9800';
        } else {
            this.charCount.style.color = '#666';
        }
    }
    
    toggleSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText || this.isTyping;
    }
    
    updateCurrentTime() {
        const timeElements = document.querySelectorAll('#currentTime');
        timeElements.forEach(el => {
            el.textContent = this.getCurrentTime();
        });
    }
    
    getCurrentTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    showToast(message) {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 5px;
            z-index: 1001;
            animation: slideInRight 0.3s ease-out;
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-in forwards';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }
}

// Add toast animations to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Initialize the chat app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
