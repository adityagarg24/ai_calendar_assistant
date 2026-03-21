# AI Calendar Assistant

A simple Python application that fetches your daily Google Calendar meetings and generates an AI-powered categorized summary.

## Phase 1: Environment Setup ✅ COMPLETED

Your environment is now ready! Here's what we've set up:

- ✅ Python 3.9.6 (working)
- ✅ Virtual environment created
- ✅ All dependencies installed:
  - Google Calendar API
  - OpenAI API
  - Date utilities
- ✅ All application files created and ready

## Phase 2: Google Calendar API Setup 🔧 NEXT STEP

**IMPORTANT: You need to complete this step before the app will work!**

### Step-by-Step Instructions:

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create or Select Project**:
   - Click "Select a project" → "New Project"
   - Name it "Calendar Assistant" → Create
3. **Enable Calendar API**:
   - Go to "APIs & Services" → "Library"
   - Search "Google Calendar API" → Enable
4. **Create Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Name it "Calendar Assistant"
   - Download the JSON file
5. **Save Credentials**:
   - Rename downloaded file to `credentials.json`
   - Move it to your `calendar-assistant` folder

## Phase 3: OpenAI API Setup 🔧 NEXT STEP

1. **Get API Key**: https://platform.openai.com/api-keys
2. **Set Environment Variable** (recommended):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or the app will prompt you for it when you run it.

## How to Run

```bash
cd calendar-assistant
source venv/bin/activate
python main.py
```

## Project Structure ✅ COMPLETE

```
calendar-assistant/
├── main.py              # Main application ✅
├── calendar_client.py   # Google Calendar integration ✅
├── ai_processor.py      # OpenAI categorization ✅
├── config.py           # Configuration settings ✅
├── requirements.txt    # Dependencies ✅
├── credentials.json    # Google API credentials (you need to add this)
├── venv/               # Virtual environment ✅
└── README.md          # This file ✅
```

## Testing Each Component

You can test individual components:

```bash
# Test Google Calendar connection (after adding credentials.json)
python calendar_client.py

# Test AI processor (will prompt for OpenAI key if not set)
python ai_processor.py
```

## Expected Output Example

Once everything is set up, running `python main.py` will show:

```
============================================================
🤖 AI CALENDAR ASSISTANT
============================================================
📅 Today: March 17, 2026

📊 DAILY SUMMARY
----------------------------------------
You have 4 meetings scheduled today, totaling approximately 3.0 hours.

🔄 RECURRING MEETINGS (2):
----------------------------------------
• Daily Standup
  ⏰ 9:00 AM - 9:30 AM (30 min)
  📋 Daily team sync meeting

• Weekly Team Review
  ⏰ 2:00 PM - 3:00 PM (60 min)

🆕 NEW MEETINGS (1):
----------------------------------------
• Client Presentation
  ⏰ 10:00 AM - 11:00 AM (60 min)
  📋 Product demo and Q&A
  👥 5 attendees

❓ MEETINGS WITHOUT AGENDA (1):
----------------------------------------
• Coffee Chat
  ⏰ 4:00 PM - 4:30 PM (30 min)

📈 STATISTICS
----------------------------------------
Total meetings: 4
Total time: 3.0 hours
Recurring: 2
New: 2
With agenda: 2
Without agenda: 2

============================================================
✨ Have a productive day!
============================================================