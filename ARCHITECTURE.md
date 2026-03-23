# AI Calendar Assistant - Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI CALENDAR ASSISTANT                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER BROWSER  │    │   VERCEL CLOUD  │    │  EXTERNAL APIs  │
│                 │    │                 │    │                 │
│ • Web Interface │◄──►│ • Flask App     │◄──►│ • Google Cal API│
│ • JavaScript    │    │ • Python Backend│    │ • OpenAI API    │
│ • HTML/CSS      │    │ • Auto Deploy   │    │ • Claude API    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
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
       │
       ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   BROWSER   │───►│ VERCEL/FLASK│───►│   GOOGLE    │
│ Loads Page  │    │ Serves HTML │    │ CALENDAR    │
└─────────────┘    └─────────────┘    │    API      │
       │                   │          └──────┬──────┘
       │                   │                 │
       ▼                   ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    USER     │    │    FLASK    │    │   EVENTS    │
│ Clicks Get  │───►│ /get_summary│◄───│   FETCHED   │
│  Summary    │    │   Route     │    │             │
└─────────────┘    └──────┬──────┘    └─────────────┘
       │                  │
       │                  ▼
       │           ┌─────────────┐    ┌─────────────┐
       │           │AI_PROCESSOR │───►│ CLAUDE/     │
       │           │ Analyzes    │    │ OPENAI API  │
       │           │   Events    │    │             │
       │           └──────┬──────┘    └─────────────┘
       │                  │                 │
       │                  ▼                 │
       │           ┌─────────────┐          │
       │           │   FLASK     │◄─────────┘
       │           │ Returns AI  │
       │           │  Analysis   │
       │           └──────┬──────┘
       │                  │
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   BROWSER   │◄───│   JSON      │
│ Displays    │    │ Response    │
│  Results    │    │             │
└─────────────┘    └─────────────┘
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
```

## 🚀 Deployment Architecture

### **Vercel Deployment:**
```
┌─────────────────────────────────────────────────────────────────┐
│                        VERCEL CLOUD                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   GITHUB    │───►│   BUILD     │───►│   DEPLOY    │         │
│  │ Repository  │    │  Process    │    │  Serverless │         │
│  │             │    │             │    │  Functions  │         │
│  │• Auto sync  │    │• Install    │    │• Global CDN │         │
│  │• Webhooks   │    │  deps       │    │• Auto scale │         │
│  │• Main branch│    │• Build app  │    │• HTTPS      │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
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