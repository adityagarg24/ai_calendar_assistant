# Configuration file for Calendar Assistant

# Google Calendar API settings
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# AI API settings
OPENAI_API_KEY = None  # Will be set from environment variable or user input
CLAUDE_API_KEY = None  # Will be set from environment variable or user input

# Calendar settings
TIMEZONE = 'Asia/Calcutta'  # Change this to your timezone if different

# Output settings
EMOJI_ENABLED = True