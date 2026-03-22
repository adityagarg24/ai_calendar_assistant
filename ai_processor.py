"""
AI integration for categorizing and summarizing calendar events
Supports both OpenAI and Claude/Anthropic APIs
"""

import os
import json
from datetime import datetime
from config import OPENAI_API_KEY, CLAUDE_API_KEY

# Try to import both AI libraries
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False


class AIProcessor:
    def __init__(self):
        self.openai_client = None
        self.claude_client = None
        self.ai_provider = None
        self._setup_ai()
    
    def _setup_ai(self):
        """Initialize AI client (try Claude first, then OpenAI)"""
        # Try Claude first
        if self._setup_claude():
            return True
        
        # Fallback to OpenAI
        if self._setup_openai():
            return True
        
        print("❌ No AI provider available. Using fallback categorization.")
        return False
    
    def _setup_claude(self):
        """Initialize Claude client"""
        if not CLAUDE_AVAILABLE:
            return False
            
        api_key = CLAUDE_API_KEY or os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            # Check if user has a Claude key that looks like it
            potential_key = os.getenv('OPENAI_API_KEY')
            if potential_key and potential_key.startswith('sk-ant-'):
                api_key = potential_key
                print("🔄 Detected Claude API key in OPENAI_API_KEY environment variable")
        
        if not api_key:
            # Don't prompt for input in web app context
            return False
        
        if api_key:
            try:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
                # Skip test connection to avoid hanging - just initialize
                print("✅ Claude client initialized successfully!")
                self.ai_provider = "claude"
                return True
            except Exception as e:
                print(f"❌ Error initializing Claude: {e}")
                return False
        
        return False
    
    def _setup_openai(self):
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            return False
            
        api_key = OPENAI_API_KEY or os.getenv('OPENAI_API_KEY')
        
        # Skip if this looks like a Claude key
        if api_key and api_key.startswith('sk-ant-'):
            return False
        
        if not api_key:
            # Don't prompt for input in web app context
            return False
        
        if api_key and not api_key.startswith('sk-ant-'):
            try:
                self.openai_client = OpenAI(api_key=api_key)
                print("✅ OpenAI client initialized successfully!")
                self.ai_provider = "openai"
                return True
            except Exception as e:
                print(f"❌ Error initializing OpenAI: {e}")
                return False
        
        return False
    
    def categorize_events(self, events):
        """Categorize events using AI"""
        if not events:
            return self._fallback_categorization(events)
        
        if self.ai_provider == "claude":
            return self._categorize_with_claude(events)
        elif self.ai_provider == "openai":
            return self._categorize_with_openai(events)
        else:
            return self._fallback_categorization(events)
    
    def _categorize_with_claude(self, events):
        """Categorize events using Claude"""
        try:
            events_text = self._format_events_for_ai(events)
            
            prompt = f"""Analyze these calendar events for a Product Manager and provide detailed actionable insights. Return ONLY a JSON response with this exact structure:

{{
    "recurring_meetings": [list of event IDs that are recurring],
    "new_meetings": [list of event IDs that are new/one-time],
    "meetings_with_agenda": [list of event IDs that have clear agenda/description],
    "meetings_without_agenda": [list of event IDs that lack agenda/description],
    "summary": "PM-focused analysis with exactly 6 bullet points separated by newlines. Each point on separate line with proper line breaks."
}}

Events to analyze:
{events_text}

Create a summary with exactly 6 bullet points covering:
• Day intensity assessment (busy/moderate/light) with specific reasoning
• Best focus time windows with exact time ranges (e.g. 9:00-10:30 AM)
• Meeting overlap analysis - identify specific conflicts and timing issues
• Agenda quality evaluation - which meetings lack preparation
• Strategic productivity recommendations for the PM
• Meeting distribution insights and energy management tips

CRITICAL FORMATTING RULES:
- Exactly 6 bullet points maximum
- Use \\n between each bullet point for proper line breaks
- Each bullet point starts with emoji and bullet symbol
- Maximum 20 words per bullet point
- No special characters that break JSON parsing
- Format: "• 🔥 Point 1\\n• 📊 Point 2\\n• 🎯 Point 3\\n• ⚠️ Point 4\\n• 💡 Point 5\\n• ⏰ Point 6"

Return only the JSON, no other text."""

            response = self.claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            ai_response = response.content[0].text
            return self._parse_ai_response(ai_response, events)
            
        except Exception as e:
            print(f"⚠️  Claude categorization failed: {e}")
            print("Falling back to rule-based categorization...")
            return self._fallback_categorization(events)
    
    def _categorize_with_openai(self, events):
        """Categorize events using OpenAI"""
        try:
            events_text = self._format_events_for_ai(events)
            
            prompt = f"""Analyze these calendar events for a Product Manager and provide actionable insights. Return a JSON response with this exact structure:

{{
    "recurring_meetings": [list of event IDs that are recurring],
    "new_meetings": [list of event IDs that are new/one-time],
    "meetings_with_agenda": [list of event IDs that have clear agenda/description],
    "meetings_without_agenda": [list of event IDs that lack agenda/description],
    "summary": "6-7 bullet points with PM-focused insights. Use emojis and be concise. Include: day intensity, focus time windows, meeting overlaps, agenda gaps, and productivity tips."
}}

Events to analyze:
{events_text}

Create a summary with bullet points covering:
• Day intensity (busy/light/moderate)
• Best focus time windows
• Meeting overlaps or conflicts
• Meetings lacking agendas
• Productivity recommendations
• Meeting distribution insights

Keep each point under 15 words. Use relevant emojis. Be direct and actionable for a PM."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a calendar assistant for Product Managers. Provide concise, actionable insights with bullet points and emojis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response, events)
            
        except Exception as e:
            print(f"⚠️  OpenAI categorization failed: {e}")
            print("Falling back to rule-based categorization...")
            return self._fallback_categorization(events)
    
    def _format_events_for_ai(self, events):
        """Format events for AI analysis"""
        formatted_events = []
        
        for event in events:
            event_info = f"""
ID: {event['id']}
Title: {event['summary']}
Time: {event['start_time'].strftime('%I:%M %p')} - {event['end_time'].strftime('%I:%M %p')}
Recurring: {event['recurring']}
Description: {event['description'][:200] if event['description'] else 'None'}
Attendees: {event['attendees']}
"""
            formatted_events.append(event_info.strip())
        
        return "\n\n".join(formatted_events)
    
    def _parse_ai_response(self, ai_response, events):
        """Parse AI response and create categorization"""
        try:
            # Try to extract JSON from the response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                ai_data = json.loads(json_str)
                
                # Create event lookup
                event_lookup = {event['id']: event for event in events}
                
                categorization = {
                    'recurring_meetings': [event_lookup[eid] for eid in ai_data.get('recurring_meetings', []) if eid in event_lookup],
                    'new_meetings': [event_lookup[eid] for eid in ai_data.get('new_meetings', []) if eid in event_lookup],
                    'meetings_with_agenda': [event_lookup[eid] for eid in ai_data.get('meetings_with_agenda', []) if eid in event_lookup],
                    'meetings_without_agenda': [event_lookup[eid] for eid in ai_data.get('meetings_without_agenda', []) if eid in event_lookup],
                    'summary': ai_data.get('summary', 'AI-generated summary not available')
                }
                
                return categorization
            else:
                raise ValueError("No valid JSON found in AI response")
                
        except Exception as e:
            print(f"⚠️  Could not parse AI response: {e}")
            return self._fallback_categorization(events)
    
    def _fallback_categorization(self, events):
        """Rule-based categorization when AI is not available"""
        if not events:
            return {
                'recurring_meetings': [],
                'new_meetings': [],
                'meetings_with_agenda': [],
                'meetings_without_agenda': [],
                'summary': 'No meetings scheduled for today.'
            }
        
        recurring = [e for e in events if e['recurring']]
        new_meetings = [e for e in events if not e['recurring']]
        with_agenda = [e for e in events if e['description'] and len(e['description'].strip()) > 10]
        without_agenda = [e for e in events if not e['description'] or len(e['description'].strip()) <= 10]
        
        # Generate simple summary
        total_meetings = len(events)
        total_hours = sum([(e['end_time'] - e['start_time']).total_seconds() / 3600 for e in events])
        
        if self.ai_provider:
            summary = f"AI-powered analysis: You have {total_meetings} meetings scheduled today, totaling approximately {total_hours:.1f} hours."
        else:
            summary = f"You have {total_meetings} meetings scheduled today, totaling approximately {total_hours:.1f} hours."
        
        return {
            'recurring_meetings': recurring,
            'new_meetings': new_meetings,
            'meetings_with_agenda': with_agenda,
            'meetings_without_agenda': without_agenda,
            'summary': summary
        }


def test_ai_processor():
    """Test function for AI processor"""
    print("🧪 Testing AI processor...")
    
    # Create sample events for testing
    sample_events = [
        {
            'id': 'test1',
            'summary': 'Daily Standup',
            'description': 'Daily team sync meeting',
            'start_time': datetime.now().replace(hour=9, minute=0),
            'end_time': datetime.now().replace(hour=9, minute=30),
            'recurring': True,
            'attendees': 5
        },
        {
            'id': 'test2',
            'summary': 'Client Meeting',
            'description': '',
            'start_time': datetime.now().replace(hour=14, minute=0),
            'end_time': datetime.now().replace(hour=15, minute=0),
            'recurring': False,
            'attendees': 3
        }
    ]
    
    processor = AIProcessor()
    
    if processor.ai_provider:
        print(f"✅ AI processor initialized successfully using {processor.ai_provider.upper()}!")
        categorization = processor.categorize_events(sample_events)
        print(f"📊 Sample categorization: {len(categorization['recurring_meetings'])} recurring, {len(categorization['new_meetings'])} new")
        return True
    else:
        print("⚠️  AI processor using fallback mode")
        categorization = processor.categorize_events(sample_events)
        print(f"📊 Fallback categorization: {len(categorization['recurring_meetings'])} recurring, {len(categorization['new_meetings'])} new")
        return False


if __name__ == "__main__":
    test_ai_processor()