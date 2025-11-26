from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

# Try to import from config file
try:
    from config import GEMINI_API_KEY as CONFIG_API_KEY
except ImportError:
    CONFIG_API_KEY = None

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class GeminiChatbot:
    def __init__(self, api_key=None):
        self.api_key = api_key or CONFIG_API_KEY or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required")
        
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
    
    def send_message(self, message):
        """Send a message to the Gemini API and return the response"""
        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": message
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0]['text']
            
            return "Sorry, I couldn't generate a response. Please try again."
            
        except requests.exceptions.RequestException as e:
            return f"Error connecting to API: {str(e)}"
        except json.JSONDecodeError:
            return "Error parsing API response. Please try again."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

# Initialize chatbot
try:
    chatbot = GeminiChatbot()
    chatbot_available = True
except ValueError as e:
    print(f"Warning: {e}")
    chatbot_available = False

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        if not chatbot_available:
            return jsonify({
                'success': False,
                'error': 'Chatbot not available. Please check API key configuration.'
            }), 500
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Get response from Gemini
        response = chatbot.send_message(message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/status')
def status():
    """Check API status"""
    return jsonify({
        'status': 'online',
        'chatbot_available': chatbot_available,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🤖 Starting CAD AI Chatbot Web Server...")
    print("=" * 50)
    
    if chatbot_available:
        print("✅ Gemini API configured successfully!")
        print("🌐 Starting web server...")
        print("📱 Open your browser and go to: http://localhost:5000")
    else:
        print("❌ Gemini API not configured!")
        print("Please set your API key in config.py or as environment variable")
        print("🌐 Web server will start but chatbot functionality will be limited")
    
    print("=" * 50)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
