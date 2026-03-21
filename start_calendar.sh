#!/bin/bash

# AI Calendar Assistant Startup Script
# This script makes it super easy to run your calendar assistant!

echo "🤖 AI Calendar Assistant Startup"
echo "=================================="
echo ""

# Navigate to the project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Project directory: $SCRIPT_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please make sure you're in the correct directory."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Prompt for Claude API key (hidden input for security)
echo "🔑 Please enter your Claude API key:"
echo "(Your typing will be hidden for security)"
read -s CLAUDE_API_KEY

if [ -z "$CLAUDE_API_KEY" ]; then
    echo "❌ No API key provided. Exiting..."
    exit 1
fi

# Export the API key
export CLAUDE_API_KEY="$CLAUDE_API_KEY"
echo "✅ API key set successfully"
echo ""

# Check if all required files exist
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found!"
    exit 1
fi

if [ ! -f "credentials.json" ]; then
    echo "⚠️  Warning: credentials.json not found!"
    echo "   Make sure you have Google Calendar credentials set up."
    echo ""
fi

# Start the Flask application
echo "🚀 Starting AI Calendar Assistant..."
echo "📱 The web app will open at: http://localhost:5001"
echo "⏹️  Press Ctrl+C to stop the server when you're done"
echo ""

# Open browser after a short delay (in background)
(sleep 3 && open http://localhost:5001) &

# Start the Flask app
python app.py