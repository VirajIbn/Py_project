# Python Projects Collection

This repository contains multiple Python projects including a Snake game and a Gemini AI chatbot.

## 🐍 Snake Game

A classic Snake game implementation using Python and Pygame.

### Snake Game Features
- Classic snake gameplay with smooth movement
- Score tracking
- Game over detection (wall collision and self-collision)
- Pause functionality
- Restart capability
- Clean, colorful graphics

### How to Play Snake
1. Run the game: `python snake_game.py`
2. Use arrow keys to control the snake
3. Game controls:
   - **SPACE**: Pause/Resume game (or restart after game over)
   - **ESC**: Quit the game

## 🤖 Gemini AI Chatbot

An intelligent chatbot powered by Google's Gemini AI API.

### Chatbot Features
- Interactive chat interface
- Chat history tracking
- Error handling and API key management
- Simple and advanced chatbot versions
- Environment variable configuration

### How to Use the Chatbot

#### Method 1: Environment Variable (Recommended)
1. Get your API key from: https://makersuite.google.com/app/apikey
2. Set environment variable:
   - **Windows**: `set GEMINI_API_KEY=your_api_key_here`
   - **Linux/Mac**: `export GEMINI_API_KEY=your_api_key_here`
3. Run: `python chatbot.py`

#### Method 2: Direct API Key
1. Edit `config.py` and replace `YOUR_API_KEY_HERE` with your actual API key
2. Or edit `simple_chatbot.py` and update the `API_KEY` variable
3. Run the desired chatbot script

### Chatbot Commands
- Type your message to chat with AI
- Type `quit`, `exit`, or `bye` to end the conversation
- Type `clear` to clear chat history
- Type `history` to see chat history

## 🚀 Installation

1. Make sure you have Python 3.6 or higher installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Files

- `snake_game.py` - Complete Snake game with pygame
- `chatbot.py` - Full-featured interactive chatbot
- `simple_chatbot.py` - Simple one-function chatbot example
- `config.py` - Configuration file for API keys
- `requirements.txt` - Python dependencies

## 🎮 Game Features

### Snake Game
- **Smooth Movement**: Consistent 10 FPS gameplay
- **Collision Detection**: Precise wall and self-collision detection
- **Visual Feedback**: Clear game over screen with restart option
- **Score Display**: Real-time score tracking
- **Pause Functionality**: Pause the game anytime with spacebar

### Chatbot
- **API Integration**: Uses Google's Gemini 2.0 Flash model
- **Error Handling**: Robust error handling for network issues
- **User-Friendly**: Intuitive command-line interface
- **History Management**: Track and manage conversation history

Enjoy both the Snake game and chatting with AI! 🐍🤖
