# AI Calendar Assistant - Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI CALENDAR ASSISTANT                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER BROWSER  │    │   VERCEL CLOUD  │    │  EXTERNAL APIs  │
│                 │    │                 │    │                 │
│ • Web Interface │◄─1─│ • Flask App     │◄─2─│ • Google Cal API│
│ • JavaScript    │    │ • Python Backend│    │ • OpenAI API    │
│ • HTML/CSS      │  3 │ • Auto Deploy   │  4 │ • Claude API    │
└─────────────────┘◄───└─────────────────┘◄───└─────────────────┘

Flow Steps:
1. User requests → Vercel Flask App
2. Flask App → External APIs (Google/AI)
3. API responses → Flask App
4. Processed results → User Browser
```

## 📊 Detailed Component Flow

### 1. **Frontend Layer (User Interface)**
```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND COMPONENTS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   HTML      │  │    CSS      │  │ JavaScript  │             │
│  │ Templates   │  │ Styling     │  │ Interactions│             │
│  │             │  │             │  │             │             │
│  │• index.html │  │• style.css  │  │• AJAX calls │             │
│  │• Forms      │  │• Gmail      │  │• Dynamic UI │             │
│  │• Results    │  │  inspired   │  │• Event      │             │
│  │  display    │  │  colors     │  │  handlers   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. **Backend Layer (Flask Application)**
```
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND COMPONENTS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   app.py    │  │ai_processor │  │calendar_    │             │
│  │ Flask Routes│  │    .py      │  │client.py    │             │
│  │             │  │             │  │             │             │
│  │• /          │  │• AI Logic   │  │• Google API │             │
│  │• /get_      │  │• Claude/    │  │• OAuth Flow │             │
│  │  summary    │  │  OpenAI     │  │• Event      │             │
│  │• /draft_    │  │• Email      │  │  Fetching   │             │
│  │  email      │  │  Generation │  │• Token Mgmt │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  config.py  │  │mock_data.py │  │   main.py   │             │
│  │Configuration│  │Demo Events  │  │CLI Version  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. **External Services Integration**
```
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   GOOGLE    │  │   OPENAI    │  │   CLAUDE    │             │
│  │ CALENDAR    │  │     API     │  │     API     │             │
│  │     API     │  │             │  │             │             │
│  │             │  │• GPT-3.5    │  │• Claude-3   │             │
│  │• OAuth 2.0  │  │• Event      │  │• Haiku      │             │
│  │• Events     │  │  Analysis   │  │• Email      │             │
│  │• Read/Write │  │• Email      │  │  Drafting   │             │
│  │• Real-time  │  │  Drafting   │  │• Smart      │             │
│  │  Access     │  │• Insights   │  │  Analysis   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

### **Complete User Journey:**

```
┌─────────────┐
│    USER     │
│  Opens App  │
└──────┬──────┘
       │ 1
       ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   BROWSER   │─2─►│ VERCEL/FLASK│─3─►│   GOOGLE    │
│ Loads Page  │    │ Serves HTML │    │ CALENDAR    │
└─────────────┘    └─────────────┘    │    API      │
       │                   │          └──────┬──────┘
       │ 4                 │ 5               │ 6
       ▼                   ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    USER     │    │    FLASK    │    │   EVENTS    │
│ Clicks Get  │─7─►│ /get_summary│◄─8─│   FETCHED   │
│  Summary    │    │   Route     │    │             │
└─────────────┘    └──────┬──────┘    └─────────────┘
       │                  │ 9
       │ 13               ▼
       │           ┌─────────────┐    ┌─────────────┐
       │           │AI_PROCESSOR │─10►│ CLAUDE/     │
       │           │ Analyzes    │    │ OPENAI API  │
       │           │   Events    │    │             │
       │           └──────┬──────┘    └─────────────┘
       │                  │ 12               │ 11
       │                  ▼                  │
       │           ┌─────────────┐           │
       │           │   FLASK     │◄──────────┘
       │           │ Returns AI  │
       │           │  Analysis   │
       │           └──────┬──────┘
       │                  │ 14
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   BROWSER   │◄15─│   JSON      │
│ Displays    │    │ Response    │
│  Results    │    │             │
└─────────────┘    └─────────────┘

Flow Steps:
1. User opens application
2. Browser requests page from Vercel
3. Flask serves HTML/CSS/JS
4. User clicks "Get Summary"
5. Browser sends AJAX request
6. Flask requests calendar events
7. Google API returns events
8. Events sent to Flask
9. Flask calls AI Processor
10. AI Processor queries Claude/OpenAI
11. AI returns analysis
12. Analysis sent back to Flask
13. Flask formats response
14. JSON response prepared
15. Results displayed to user
```

## 🧩 Core Components Breakdown

### **1. Flask Application (app.py)**
- **Purpose:** Main web server and API endpoints
- **Key Routes:**
  - `/` - Serves main interface
  - `/get_summary` - Fetches and analyzes calendar events
  - `/draft_email` - Generates agenda request emails
- **Features:**
  - Session management
  - Error handling
  - CORS support
  - Demo mode

### **2. AI Processor (ai_processor.py)**
- **Purpose:** AI integration and analysis engine
- **Capabilities:**
  - Event categorization (recurring vs new)
  - Agenda quality assessment
  - Smart email generation
  - Fallback rule-based logic
- **AI Providers:**
  - Claude (Anthropic) - Primary
  - OpenAI GPT-3.5 - Fallback
  - Rule-based - Final fallback

### **3. Calendar Client (calendar_client.py)**
- **Purpose:** Google Calendar API integration
- **Functions:**
  - OAuth 2.0 authentication
  - Event fetching and parsing
  - Token management
  - Error handling

### **4. Configuration (config.py)**
- **Purpose:** Centralized configuration management
- **Contains:**
  - API keys
  - Google OAuth credentials
  - Application settings

## 🔐 Security & Authentication Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    USER     │    │    FLASK    │    │   GOOGLE    │
│             │    │             │    │   OAUTH     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ 1. Access App    │                  │
       ├─────────────────►│                  │
       │                  │ 2. Check Token   │
       │                  ├─────────────────►│
       │                  │ 3. Redirect Auth │
       │ 4. Login Google  │◄─────────────────┤
       ├─────────────────────────────────────►│
       │ 5. Grant Access  │                  │
       │◄─────────────────────────────────────┤
       │                  │ 6. Get Token     │
       │                  │◄─────────────────┤
       │ 7. Access Granted│                  │
       │◄─────────────────┤                  │

Authentication Steps:
1. User accesses the application
2. Flask checks for existing OAuth token
3. If no token, redirect to Google OAuth
4. User logs in with Google credentials
5. User grants calendar access permissions
6. Google returns OAuth token to Flask
7. Flask grants access to calendar features
```

## 🚀 Deployment Architecture

### **Vercel Deployment:**
```
┌─────────────────────────────────────────────────────────────────┐
│                        VERCEL CLOUD                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   GITHUB    │─1─►│   BUILD     │─2─►│   DEPLOY    │         │
│  │ Repository  │    │  Process    │    │  Serverless │         │
│  │             │    │             │    │  Functions  │         │
│  │• Auto sync  │    │• Install    │    │• Global CDN │         │
│  │• Webhooks   │  3 │  deps       │  4 │• Auto scale │         │
│  │• Main branch│◄───│• Build app  │◄───│• HTTPS      │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Deployment Steps:
1. Code pushed to GitHub main branch
2. Vercel webhook triggers build process
3. Dependencies installed, app built
4. Serverless functions deployed to global CDN
```

## 📈 Performance & Scalability

### **Current Architecture Benefits:**
- ✅ **Serverless:** Auto-scaling with Vercel
- ✅ **Stateless:** No server-side sessions
- ✅ **Cached:** Static assets via CDN
- ✅ **Responsive:** Fast loading times
- ✅ **Reliable:** Multiple AI provider fallbacks

### **Scalability Considerations:**
- **API Rate Limits:** Handled with fallbacks
- **Concurrent Users:** Serverless auto-scaling
- **Data Storage:** Stateless design (no database)
- **Global Access:** CDN distribution

## 🔧 Development & Maintenance

### **Local Development:**
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
python app.py
# Access: http://localhost:5002
```

### **Deployment Process:**
```bash
# Push to GitHub
git add .
git commit -m "Update message"
git push origin main

# Vercel auto-deploys
# Live at: https://ai-calendar-assistant-flax.vercel.app/
```

## 🎯 Key Features Summary

1. **Smart Calendar Analysis** - AI-powered event categorization
2. **Email Generation** - Automated agenda request drafting
3. **Multi-AI Support** - Claude + OpenAI with fallbacks
4. **Real-time Integration** - Live Google Calendar access
5. **Responsive Design** - Gmail-inspired clean interface
6. **Demo Mode** - Mock data for testing without calendar access
7. **Error Resilience** - Multiple fallback mechanisms
8. **Serverless Deployment** - Scalable cloud architecture

This architecture provides a robust, scalable, and maintainable AI-powered calendar assistant with enterprise-grade reliability and user experience.