# 🚀 Quick Start Guide - AI Calendar Assistant

## **Super Easy Daily Usage (5 seconds!)**

### **Method 1: Double-Click Script (Recommended)**
1. **Navigate to your project folder**: `/Users/aditya.garg/Desktop/calendar-assistant`
2. **Double-click**: `start_calendar.sh`
3. **Enter your Claude API key** when prompted (typing will be hidden)
4. **Browser opens automatically** at `http://localhost:5001`
5. **Click "Get Today's Summary"** and enjoy!

### **Method 2: Terminal (Alternative)**
```bash
cd /Users/aditya.garg/Desktop/calendar-assistant
./start_calendar.sh
```

## **What the Script Does for You**
- ✅ Navigates to the correct folder
- ✅ Activates virtual environment
- ✅ Prompts for Claude API key securely
- ✅ Starts the web server
- ✅ Opens your browser automatically
- ✅ Shows helpful status messages

## **What You Need**
- 🔑 Your Claude API key (starts with `sk-ant-...`)
- 🌐 Internet connection
- ⏱️ About 5 seconds of your time

## **Stopping the App**
- Press `Ctrl+C` in the terminal window
- Or simply close the terminal window

## **Troubleshooting**

### **Script Won't Run?**
```bash
chmod +x start_calendar.sh
```

### **"Permission Denied" Error?**
Right-click the script → "Open With" → "Terminal"

### **Browser Doesn't Open?**
Manually go to: `http://localhost:5001`

### **Google Calendar Not Working?**
Make sure `credentials.json` is in your project folder

### **Claude API Issues?**
- Check your API key is correct (starts with `sk-ant-`)
- Verify you have credits in your Anthropic account

## **Your Project Structure**
```
calendar-assistant/
├── start_calendar.sh     ← Your new startup script!
├── app.py               ← Web application
├── credentials.json     ← Google Calendar credentials
├── venv/               ← Virtual environment
├── templates/          ← Web pages
├── static/            ← Styling
└── (other files...)
```

## **Daily Workflow**
1. **Morning**: Run `start_calendar.sh`
2. **Enter API key**: When prompted
3. **Get insights**: Click "Get Today's Summary"
4. **Plan your day**: Based on AI analysis
5. **Close**: Press `Ctrl+C` when done

---

**🎉 That's it! Your AI Calendar Assistant is now super easy to use daily!**