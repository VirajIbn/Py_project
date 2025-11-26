import requests
import json
import os
from typing import Optional

# Try to import from config file
try:
    from config import GEMINI_API_KEY as CONFIG_API_KEY
except ImportError:
    CONFIG_API_KEY = None

class GeminiChatbot:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini Chatbot
        
        Args:
            api_key: Your Gemini API key. If not provided, will look for GEMINI_API_KEY environment variable
        """
        self.api_key = api_key or CONFIG_API_KEY or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set GEMINI_API_KEY in config.py, as environment variable, or pass api_key parameter")
        
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        # Chat history for context
        self.chat_history = []
    
    def send_message(self, message: str) -> str:
        """
        Send a message to the Gemini API and return the response
        
        Args:
            message: The user's message
            
        Returns:
            The AI's response
        """
        try:
            # Prepare the request payload
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
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            
            # Extract the generated text
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    generated_text = candidate['content']['parts'][0]['text']
                    
                    # Add to chat history
                    self.chat_history.append({"role": "user", "content": message})
                    self.chat_history.append({"role": "assistant", "content": generated_text})
                    
                    return generated_text
            
            return "Sorry, I couldn't generate a response. Please try again."
            
        except requests.exceptions.RequestException as e:
            return f"Error connecting to API: {str(e)}"
        except json.JSONDecodeError:
            return "Error parsing API response. Please try again."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    def clear_history(self):
        """Clear the chat history"""
        self.chat_history = []
    
    def get_history(self):
        """Get the current chat history"""
        return self.chat_history

def main():
    """Main function to run the chatbot interactively"""
    print("🤖 Gemini Chatbot")
    print("=" * 50)
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'clear' to clear chat history")
    print("Type 'history' to see chat history")
    print("-" * 50)
    
    try:
        # Initialize the chatbot
        chatbot = GeminiChatbot()
        print("✅ Connected to Gemini API successfully!")
        print()
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for chatting!")
                break
            
            # Check for clear command
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                print("🗑️ Chat history cleared!")
                continue
            
            # Check for history command
            elif user_input.lower() == 'history':
                history = chatbot.get_history()
                if not history:
                    print("📝 No chat history available.")
                else:
                    print("📝 Chat History:")
                    for i, msg in enumerate(history, 1):
                        role = "You" if msg["role"] == "user" else "AI"
                        print(f"  {i}. {role}: {msg['content'][:100]}...")
                continue
            
            # Skip empty input
            elif not user_input:
                continue
            
            # Send message to AI
            print("🤖 AI: ", end="", flush=True)
            response = chatbot.send_message(user_input)
            print(response)
            print()
            
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nTo fix this:")
        print("1. Get your API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as an environment variable:")
        print("   - Windows: set GEMINI_API_KEY=your_api_key_here")
        print("   - Linux/Mac: export GEMINI_API_KEY=your_api_key_here")
        print("3. Or modify the code to include your API key directly")
    
    except KeyboardInterrupt:
        print("\n👋 Chat interrupted. Goodbye!")
    
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
