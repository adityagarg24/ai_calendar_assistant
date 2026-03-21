# 🔧 Phase 2: Google Calendar API Setup Guide

## What You Need
- A Google account (you already have this ✅)
- 5-10 minutes of your time
- Access to Google Cloud Console

## Step-by-Step Instructions

### Step 1: Go to Google Cloud Console
1. Open your web browser
2. Go to: **https://console.cloud.google.com/**
3. Sign in with your Google account

### Step 2: Create a New Project
1. Click on the **project dropdown** at the top (it might say "Select a project")
2. Click **"NEW PROJECT"**
3. Enter project name: **"Calendar Assistant"**
4. Click **"CREATE"**
5. Wait for the project to be created (30 seconds)
6. Make sure your new project is selected

### Step 3: Enable Google Calendar API
1. In the left sidebar, click **"APIs & Services"** → **"Library"**
2. In the search box, type: **"Google Calendar API"**
3. Click on **"Google Calendar API"** from the results
4. Click the blue **"ENABLE"** button
5. Wait for it to enable (30 seconds)

### Step 4: Create OAuth Credentials
1. In the left sidebar, click **"APIs & Services"** → **"Credentials"**
2. Click the blue **"+ CREATE CREDENTIALS"** button
3. Select **"OAuth client ID"**
4. If prompted about OAuth consent screen:
   - Click **"CONFIGURE CONSENT SCREEN"**
   - Choose **"External"** → **"CREATE"**
   - Fill in:
     - App name: **"Calendar Assistant"**
     - User support email: **your email**
     - Developer contact: **your email**
   - Click **"SAVE AND CONTINUE"** through all steps
   - Go back to **"Credentials"**
5. Now create OAuth client ID:
   - Application type: **"Desktop application"**
   - Name: **"Calendar Assistant"**
   - Click **"CREATE"**

### Step 5: Download Credentials File
1. After creating, you'll see a popup with your credentials
2. Click **"DOWNLOAD JSON"**
3. The file will download (usually to your Downloads folder)
4. **IMPORTANT**: Rename this file to exactly: **`credentials.json`**
5. Move this file to your `calendar-assistant` folder

### Step 6: Verify Setup
Your `calendar-assistant` folder should now look like this:
```
calendar-assistant/
├── credentials.json     ← This is the file you just added
├── main.py
├── calendar_client.py
├── ai_processor.py
├── config.py
├── requirements.txt
├── README.md
└── venv/
```

## Test Google Calendar Connection

Run this command to test if Google Calendar setup worked:

```bash
cd calendar-assistant
source venv/bin/activate
python calendar_client.py
```

**What should happen:**
1. Your web browser will open
2. Google will ask you to sign in and grant permissions
3. Choose your Google account
4. Click **"Allow"** to grant calendar access
5. You should see: **"✅ Successfully connected to Google Calendar!"**

## Troubleshooting

### Problem: "credentials.json not found"
- Make sure the file is named exactly `credentials.json` (not `credentials (1).json`)
- Make sure it's in the `calendar-assistant` folder

### Problem: "OAuth consent screen" errors
- Make sure you completed the consent screen setup in Step 4
- Try using "Internal" instead of "External" if you have a Google Workspace account

### Problem: Browser doesn't open
- Copy the URL from terminal and paste it in your browser manually

## What's Next?

Once Google Calendar is working, you'll need to set up OpenAI API (Phase 3) and then you can run your complete calendar assistant!

---

**Need help?** The error messages are usually very clear about what's wrong. Read them carefully!