# 🤖 Phase 3: OpenAI API Setup Guide

## What You Need
- An OpenAI account
- A credit card (for API usage - costs ~$0.01-0.10 per day)
- 5 minutes of your time

## Step-by-Step Instructions

### Step 1: Create OpenAI Account
1. Go to: **https://platform.openai.com/**
2. Click **"Sign up"** (or "Log in" if you have an account)
3. Create account with email or use Google/Microsoft sign-in
4. Verify your email if prompted

### Step 2: Add Payment Method
1. Once logged in, go to: **https://platform.openai.com/account/billing**
2. Click **"Add payment method"**
3. Add your credit card details
4. **Don't worry**: You'll only be charged for what you use (~$0.01-0.10 per day)

### Step 3: Get Your API Key
1. Go to: **https://platform.openai.com/api-keys**
2. Click **"+ Create new secret key"**
3. Give it a name: **"Calendar Assistant"**
4. Click **"Create secret key"**
5. **IMPORTANT**: Copy the key immediately (it starts with `sk-...`)
6. **SAVE IT SOMEWHERE SAFE** - you won't be able to see it again!

### Step 4: Set Up API Key (Choose One Method)

#### Method 1: Environment Variable (Recommended)
Open Terminal and run:
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```
Replace `your-api-key-here` with your actual API key.

#### Method 2: Let the App Ask You
- Don't set environment variable
- The app will prompt you for the API key when you run it
- You'll need to enter it each time you run the app

### Step 5: Test OpenAI Connection

Run this command to test if OpenAI setup worked:

```bash
cd calendar-assistant
source venv/bin/activate
python ai_processor.py
```

**What should happen:**
- If using environment variable: **"✅ OpenAI client initialized successfully!"**
- If not set: It will ask you to enter your API key
- You should see: **"📊 Sample categorization: X recurring, Y new"**

## Cost Information

### How Much Will This Cost?
- **Setup**: $0 (free to create account and get API key)
- **Daily usage**: $0.01 - $0.10 per day
- **Monthly**: ~$1-3 per month for daily use
- **What you get**: AI-powered meeting categorization and summaries

### Why So Cheap?
- We're only sending small text snippets (meeting titles/descriptions)
- Using GPT-3.5-turbo (cheaper than GPT-4)
- Only runs when you check your calendar (not continuously)

### Usage Monitoring
- Check usage at: **https://platform.openai.com/account/usage**
- Set spending limits at: **https://platform.openai.com/account/billing/limits**

## Troubleshooting

### Problem: "Invalid API key"
- Make sure you copied the full key (starts with `sk-`)
- Check for extra spaces or characters
- Generate a new key if needed

### Problem: "Insufficient quota"
- Add a payment method to your OpenAI account
- Check your billing limits

### Problem: Environment variable not working
- Restart your terminal after setting the variable
- Try Method 2 (let app ask for key) instead

## Alternative: Skip AI (Free Option)

If you don't want to use OpenAI, the app will still work! It will use simple rule-based categorization instead of AI. Just run the app without setting up OpenAI - it will automatically fall back to the free option.

## What's Next?

Once both Google Calendar AND OpenAI are set up, you can run your complete AI Calendar Assistant:

```bash
cd calendar-assistant
source venv/bin/activate
python main.py
```

---

**Security Note**: Never share your API key publicly or commit it to code repositories!