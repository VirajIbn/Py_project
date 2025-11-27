from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

# Try to import from config file
try:
    from config import GEMINI_API_KEY as CONFIG_API_KEY
except ImportError:
    CONFIG_API_KEY = None

# Import Google Generative AI SDK
try:
    from google import genai
except ImportError:
    genai = None

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class GeminiChatbot:
    def __init__(self, api_key=None):
        if genai is None:
            raise ValueError("google-genai package is required. Install it with: pip install -q -U google-genai")
        
        self.api_key = api_key or CONFIG_API_KEY or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required")
        
        # Initialize the client with API key (as shown in documentation)
        self.client = genai.Client(api_key=self.api_key)
        
        # Try different models in order of preference (starting with gemini-2.5-flash from docs)
        self.models = [
            'gemini-2.5-flash',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        self.current_model = None
    
    def send_message(self, message):
        """Send a message to the Gemini API and return the response"""
        # Try each model until one works
        last_error = None
        for model_name in self.models:
            try:
                # Use the SDK method as shown in documentation
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=message
                )
                
                # Extract text from response (as shown in docs: response.text)
                if hasattr(response, 'text') and response.text:
                    self.current_model = model_name
                    return response.text
                else:
                    # Fallback: try to extract from candidates if text attribute doesn't exist
                    if hasattr(response, 'candidates') and len(response.candidates) > 0:
                        candidate = response.candidates[0]
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            parts = candidate.content.parts
                            if len(parts) > 0 and hasattr(parts[0], 'text'):
                                self.current_model = model_name
                                return parts[0].text
                    
                    # If we got here but no text, try next model
                    if model_name != self.models[-1]:
                        continue
                    else:
                        return "Received response but could not extract text content."
                    
            except Exception as e:
                # If this model fails, try the next one
                error_msg = str(e)
                last_error = error_msg
                if model_name != self.models[-1]:
                    continue
                else:
                    return f"Error with all models. Last error: {error_msg}"
        
        # If all models failed, return the last error
        return last_error or "Unable to generate response from any available model."

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
