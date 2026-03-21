# 🤖 Claude/Anthropic API Setup Guide

## What You Need
- An Anthropic account
- A credit card (for API usage - costs ~$0.01-0.10 per day)
- 5 minutes of your time

## Step-by-Step Instructions

### Step 1: Create Anthropic Account
1. Go to: **https://console.anthropic.com/**
2. Click **"Sign up"** (or "Log in" if you have an account)
3. Create account with email or use Google sign-in
4. Verify your email if prompted

### Step 2: Add Payment Method
1. Once logged in, go to: **https://console.anthropic.com/account/billing**
2. Click **"Add payment method"**
3. Add your credit card details
4. **Don't worry**: You'll only be charged for what you use (~$0.01-0.10 per day)

### Step 3: Get Your API Key
1. Go to: **https://console.anthropic.com/account/keys**
2. Click **"+ Create Key"**
3. Give it a name: **"Calendar Assistant"**
4. Click **"Create Key"**
5. **IMPORTANT**: Copy the key immediately (it starts with `sk-ant-...`)
6. **SAVE IT SOMEWHERE SAFE** - you won't be able to see it again!

### Step 4: Set Up API Key (Choose One Method)

#### Method 1: Environment Variable (Recommended)
Open Terminal and run:
```bash
echo 'export CLAUDE_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```
Replace `your-api-key-here` with your actual Claude API key.

#### Method 2: Alternative Environment Variable Name
You can also use:
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### Method 3: Let the App Ask You
- Don't set environment variable
- The app will prompt you for the API key when you run it
- You'll need to enter it each time you run the app

### Step 5: Test Claude Connection

Run this command to test if Claude setup worked:

```bash
cd calendar-assistant
source venv/bin/activate
python ai_processor.py
```

**What should happen:**
- **"✅ Claude client initialized successfully!"**
- **"✅ AI processor initialized successfully using CLAUDE!"**
- You should see: **"📊 Sample categorization: X recurring, Y new"**

## Cost Information

### How Much Will This Cost?
- **Setup**: $0 (free to create account and get API key)
- **Daily usage**: $0.01 - $0.10 per day
- **Monthly**: ~$1-3 per month for daily use
- **What you get**: Claude-powered meeting categorization and summaries

### Why So Cheap?
- We're only sending small text snippets (meeting titles/descriptions)
- Using Claude 3 Haiku (fastest and most cost-effective model)
- Only runs when you check your calendar (not continuously)

### Usage Monitoring
- Check usage at: **https://console.anthropic.com/account/usage**
- Set spending limits at: **https://console.anthropic.com/account/billing**

## Troubleshooting

### Problem: "Invalid API key"
- Make sure you copied the full key (starts with `sk-ant-`)
- Check for extra spaces or characters
- Generate a new key if needed

### Problem: "Insufficient quota"
- Add a payment method to your Anthropic account
- Check your billing limits

### Problem: Environment variable not working
- Restart your terminal after setting the variable
- Try Method 3 (let app ask for key) instead

## Advantages of Claude

- **Better at following instructions**: More precise JSON formatting
- **Faster responses**: Claude 3 Haiku is very quick
- **Better reasoning**: Often provides more insightful meeting analysis
- **Cost-effective**: Similar pricing to OpenAI but often better results

## What's Next?

Once Claude is set up, you can run your complete AI Calendar Assistant:

```bash
cd calendar-assistant
source venv/bin/activate
export CLAUDE_API_KEY="your-key-here"
python main.py
```

You should see **"✅ Claude client initialized successfully!"** and get AI-powered categorization!

---

**Security Note**: Never share your API key publicly or commit it to code repositories!