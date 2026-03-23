#!/usr/bin/env python3
"""
Flask Web App for AI Calendar Assistant
"""

import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime
import traceback
from calendar_client import CalendarClient
from ai_processor import AIProcessor
from mock_data import get_mock_events, get_mock_summary, get_rule_based_summary

app = Flask(__name__)

# Global variables to store instances
calendar_client = None
ai_processor = None

def get_user_email():
    """Get user's email from Google Calendar"""
    try:
        # Initialize calendar client if needed
        global calendar_client
        if not calendar_client:
            calendar_client = CalendarClient()
            calendar_client.authenticate()
        
        if calendar_client and calendar_client.service:
            # Try to get user info from calendar service
            calendar_list = calendar_client.service.calendarList().list().execute()
            for calendar in calendar_list.get('items', []):
                if calendar.get('primary'):
                    return calendar.get('id', 'Connected')
        return 'Connected'
    except Exception:
        return 'Not connected'

@app.route('/')
def index():
    """Main page"""
    today = datetime.now().strftime('%B %d, %Y')
    email = get_user_email()
    return render_template('index.html', today=today, email=email)

@app.route('/get_summary')
def get_summary():
    """Get calendar summary via AJAX - supports both demo and live modes"""
    global calendar_client, ai_processor
    
    # Check if demo mode is requested
    demo_mode = request.args.get('demo', 'false').lower() == 'true'
    claude_api_key = request.args.get('claude_key', '').strip()
    
    try:
        if demo_mode:
            # Use mock data for demo
            events = get_mock_events()
            
            # Use AI if API key provided, otherwise rule-based
            if claude_api_key:
                try:
                    # Temporarily set API key for this request
                    os.environ['CLAUDE_API_KEY'] = claude_api_key
                    # Create new AI processor instance for each request to avoid hanging
                    ai_processor = AIProcessor()
                    print(f"🤖 Starting AI analysis for {len(events)} events...")
                    categorization = ai_processor.categorize_events(events)
                    ai_provider = 'claude'
                    print("✅ AI analysis completed successfully!")
                except Exception as e:
                    print(f"❌ AI analysis failed: {e}")
                    # Check if it's an authentication error
                    error_msg = str(e)
                    if 'authentication_error' in error_msg or 'invalid x-api-key' in error_msg or '401' in error_msg:
                        return jsonify({
                            'error': True,
                            'message': 'Invalid Claude API key. Please check your API key and try again.'
                        })
                    else:
                        # Fall back to rule-based for other errors
                        print("🔄 Falling back to rule-based analysis...")
                        categorization = categorize_events_rule_based(events)
                        ai_provider = 'rule-based'
            else:
                categorization = categorize_events_rule_based(events)
                ai_provider = 'rule-based'
                
        else:
            # Original live mode logic
            if not calendar_client:
                calendar_client = CalendarClient()
                if not calendar_client.authenticate():
                    return jsonify({
                        'error': True,
                        'message': 'Failed to connect to Google Calendar. Please check your credentials.json file.'
                    })
            
            events = calendar_client.get_todays_events()
            
            if not events:
                return jsonify({
                    'error': False,
                    'message': 'No meetings scheduled for today! 🎉 Enjoy your free day!',
                    'events': [],
                    'summary': 'No meetings scheduled for today.',
                    'stats': {
                        'total': 0,
                        'hours': 0,
                        'recurring': 0,
                        'new': 0,
                        'with_agenda': 0,
                        'without_agenda': 0
                    }
                })
            
            # Use AI if API key provided, otherwise rule-based
            if claude_api_key:
                try:
                    # Temporarily set API key for this request
                    os.environ['CLAUDE_API_KEY'] = claude_api_key
                    ai_processor = AIProcessor()
                    categorization = ai_processor.categorize_events(events)
                    ai_provider = 'claude'
                except Exception as e:
                    # Check if it's an authentication error
                    error_msg = str(e)
                    if 'authentication_error' in error_msg or 'invalid x-api-key' in error_msg or '401' in error_msg:
                        return jsonify({
                            'error': True,
                            'message': 'Invalid Claude API key. Please check your API key and try again.'
                        })
                    else:
                        # Fall back to rule-based for other errors
                        categorization = categorize_events_rule_based(events)
                        ai_provider = 'rule-based'
            else:
                # Use rule-based categorization for live mode without API key
                categorization = categorize_events_rule_based(events)
                ai_provider = 'rule-based'
        
        # Calculate statistics
        all_events = categorization['recurring_meetings'] + categorization['new_meetings']
        total_hours = sum([(e['end_time'] - e['start_time']).total_seconds() / 3600 for e in all_events])
        
        # Detect overlapping meetings
        overlapping_meetings = detect_overlapping_meetings(all_events)
        
        # Format events for display
        formatted_events = {
            'recurring': [format_event(e) for e in categorization['recurring_meetings']],
            'new': [format_event(e) for e in categorization['new_meetings']],
            'with_agenda': [format_event(e) for e in categorization['meetings_with_agenda']],
            'without_agenda': [format_event(e) for e in categorization['meetings_without_agenda']]
        }
        
        # Format overlapping meetings for frontend
        formatted_overlapping = []
        for group in overlapping_meetings:
            formatted_group = [format_event(e) for e in group]
            formatted_overlapping.append(formatted_group)
        
        stats = {
            'total': len(all_events),
            'hours': round(total_hours, 1),
            'recurring': len(categorization['recurring_meetings']),
            'new': len(categorization['new_meetings']),
            'with_agenda': len(categorization['meetings_with_agenda']),
            'without_agenda': len(categorization['meetings_without_agenda'])
        }
        
        return jsonify({
            'error': False,
            'events': formatted_events,
            'summary': categorization['summary'],
            'stats': stats,
            'ai_provider': ai_provider,
            'demo_mode': demo_mode,
            'overlapping_meetings': formatted_overlapping
        })
        
    except Exception as e:
        error_msg = str(e)
        if 'credentials.json' in error_msg:
            error_msg = 'Google Calendar credentials not found. Using demo mode with sample data.'
            # Fall back to demo mode
            return get_summary_demo_fallback()
        elif 'API key' in error_msg:
            error_msg = 'AI API key not configured. Using rule-based categorization.'
        elif 'No module named' in error_msg:
            error_msg = 'Missing dependencies. Please run: pip install -r requirements.txt'
        else:
            error_msg = f'An error occurred: {error_msg}'
        
        return jsonify({
            'error': True,
            'message': error_msg,
            'details': traceback.format_exc() if app.debug else None
        })

def generate_dynamic_summary(events):
    """Generate dynamic summary based on actual events passed"""
    total = len(events)
    recurring = len([e for e in events if e.get('recurring', False)])
    new = total - recurring
    with_agenda = len([e for e in events if e.get('description', '').strip()])
    
    if total == 0:
        return "No meetings scheduled for today! 🎉 Enjoy your free day!"
    elif total == 1:
        agenda_text = "has a detailed agenda" if with_agenda == 1 else "has no agenda"
        meeting_type = "recurring" if recurring == 1 else "new"
        return f"You have 1 {meeting_type} meeting today that {agenda_text}."
    else:
        return f"You have {total} meetings today. {recurring} are recurring, {new} are new. {with_agenda} meetings have detailed agendas."

def categorize_events_rule_based(events):
    """Rule-based event categorization that works for both demo and live data"""
    recurring_meetings = [e for e in events if e.get('recurring', False)]
    new_meetings = [e for e in events if not e.get('recurring', False)]
    meetings_with_agenda = [e for e in events if e.get('description', '').strip()]
    meetings_without_agenda = [e for e in events if not e.get('description', '').strip()]
    
    return {
        'recurring_meetings': recurring_meetings,
        'new_meetings': new_meetings,
        'meetings_with_agenda': meetings_with_agenda,
        'meetings_without_agenda': meetings_without_agenda,
        'summary': generate_dynamic_summary(events)
    }

def get_summary_demo_fallback():
    """Fallback to demo mode when live mode fails"""
    events = get_mock_events()
    categorization = categorize_events_rule_based(events)
    
    all_events = categorization['recurring_meetings'] + categorization['new_meetings']
    total_hours = sum([(e['end_time'] - e['start_time']).total_seconds() / 3600 for e in all_events])
    
    formatted_events = {
        'recurring': [format_event(e) for e in categorization['recurring_meetings']],
        'new': [format_event(e) for e in categorization['new_meetings']],
        'with_agenda': [format_event(e) for e in categorization['meetings_with_agenda']],
        'without_agenda': [format_event(e) for e in categorization['meetings_without_agenda']]
    }
    
    stats = {
        'total': len(all_events),
        'hours': round(total_hours, 1),
        'recurring': len(categorization['recurring_meetings']),
        'new': len(categorization['new_meetings']),
        'with_agenda': len(categorization['meetings_with_agenda']),
        'without_agenda': len(categorization['meetings_without_agenda'])
    }
    
    return jsonify({
        'error': False,
        'events': formatted_events,
        'summary': categorization['summary'],
        'stats': stats,
        'ai_provider': 'rule-based',
        'demo_mode': True,
        'fallback_message': 'Switched to demo mode with sample data'
    })

def detect_overlapping_meetings(events):
    """Detect meetings that overlap in time"""
    overlapping_groups = []
    
    for i, event1 in enumerate(events):
        overlaps = []
        for j, event2 in enumerate(events):
            if i != j:
                # Check if events overlap
                start1, end1 = event1['start_time'], event1['end_time']
                start2, end2 = event2['start_time'], event2['end_time']
                
                # Events overlap if one starts before the other ends
                if start1 < end2 and start2 < end1:
                    overlaps.append(event2)
        
        # If this event has overlaps and we haven't already grouped it
        if overlaps:
            # Check if this event is already in an existing group
            already_grouped = False
            for group in overlapping_groups:
                if event1 in group:
                    already_grouped = True
                    break
            
            if not already_grouped:
                # Create new group with this event and its overlaps
                new_group = [event1] + overlaps
                # Remove duplicates while preserving order
                unique_group = []
                seen = set()
                for event in new_group:
                    event_id = event.get('id', event['summary'])
                    if event_id not in seen:
                        unique_group.append(event)
                        seen.add(event_id)
                overlapping_groups.append(unique_group)
    
    return overlapping_groups

def format_event(event):
    """Format event for display"""
    return {
        'id': event.get('id', event['summary']),
        'title': event['summary'],
        'start_time': event['start_time'].strftime('%I:%M %p').lstrip('0'),
        'end_time': event['end_time'].strftime('%I:%M %p').lstrip('0'),
        'duration': int((event['end_time'] - event['start_time']).total_seconds() / 60),
        'description': event['description'][:100] + '...' if len(event['description']) > 100 else event['description'],
        'location': event['location'],
        'attendees': event['attendees'],
        'recurring': event['recurring']
    }

@app.route('/draft_email')
def draft_email():
    """Draft email to request agenda for a meeting"""
    try:
        # Get parameters
        event_id = request.args.get('event_id', '')
        title = request.args.get('title', '')
        start_time = request.args.get('start_time', '')
        end_time = request.args.get('end_time', '')
        attendees = request.args.get('attendees', '0')
        mode = request.args.get('mode', 'rule-based')
        claude_key = request.args.get('claude_key', '').strip()
        
        if mode == 'rule-based':
            # Simple rule-based email draft with better tone
            email_draft = f"Hi,\n\nCould you share the agenda for '{title}' ({start_time} - {end_time})? It would help us come prepared.\n\nThanks!"
            
        elif mode == 'ai' and claude_key:
            # AI-powered email draft
            try:
                # Temporarily set API key
                os.environ['CLAUDE_API_KEY'] = claude_key
                ai_processor = AIProcessor()
                
                # Create context for AI
                meeting_context = {
                    'title': title,
                    'start_time': start_time,
                    'end_time': end_time,
                    'attendees': int(attendees) if attendees.isdigit() else 0
                }
                
                email_draft = ai_processor.draft_agenda_request_email(meeting_context)
                
            except Exception as e:
                print(f"❌ AI email draft failed: {e}")
                # Fall back to rule-based
                email_draft = f"Hi team,\n\nCould you please share the agenda for '{title}' scheduled on {start_time} - {end_time}? This will help us prepare better for the meeting.\n\nThanks!"
        else:
            # Default to rule-based if no valid mode
            email_draft = f"Hi team,\n\nCould you please share the agenda for '{title}' scheduled on {start_time} - {end_time}? This will help us prepare better for the meeting.\n\nThanks!"
        
        return jsonify({
            'error': False,
            'email_draft': email_draft,
            'mode_used': mode
        })
        
    except Exception as e:
        print(f"❌ Email draft error: {e}")
        return jsonify({
            'error': True,
            'message': f'Failed to generate email draft: {str(e)}'
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# Set Claude API key from environment if available (for both local and production)
claude_key = os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
if claude_key:
    os.environ['CLAUDE_API_KEY'] = claude_key

if __name__ == '__main__':
    print("🚀 Starting Calendar Assistant Web App...")
    print("📱 Open your browser to: http://localhost:5002")
    print("⏹️  Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='localhost', port=5002)
