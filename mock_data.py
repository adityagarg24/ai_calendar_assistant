#!/usr/bin/env python3
"""
Mock Calendar Data for Portfolio Demo
Gmail Calendar-inspired realistic events
"""

from datetime import datetime, timedelta

def get_mock_events():
    """Generate realistic mock calendar events for demo"""
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    mock_events = [
        # Recurring Events
        {
            'id': 'mock_event_1',
            'summary': 'Daily Standup',
            'start_time': today.replace(hour=9, minute=0),
            'end_time': today.replace(hour=9, minute=15),
            'description': 'Daily team sync - Share progress, blockers, and today\'s plans. Quick 15-min check-in with the development team.',
            'location': 'Zoom Meeting',
            'attendees': 8,
            'recurring': True
        },
        {
            'id': 'mock_event_2',
            'summary': 'Weekly Team Sync',
            'start_time': today.replace(hour=14, minute=0),
            'end_time': today.replace(hour=15, minute=0),
            'description': 'Weekly team alignment meeting. Discuss sprint progress, upcoming deadlines, and team updates.',
            'location': 'Conference Room A',
            'attendees': 12,
            'recurring': True
        },
        {
            'id': 'mock_event_3',
            'summary': 'Lunch',
            'start_time': today.replace(hour=12, minute=30),
            'end_time': today.replace(hour=13, minute=0),
            'description': '',
            'location': '',
            'attendees': 1,
            'recurring': True
        },
        
        # New Meetings
        {
            'id': 'mock_event_4',
            'summary': 'Client Demo - Syncup',
            'start_time': today.replace(hour=10, minute=30),
            'end_time': today.replace(hour=11, minute=30),
            'description': 'Product demonstration for Syncup client. Showcase new features: dashboard analytics, user management, and API integrations. Prepare demo environment and presentation slides.',
            'location': 'Google Meet',
            'attendees': 6,
            'recurring': False
        },
        {
            'id': 'mock_event_5',
            'summary': 'Quick sync with ABC',
            'start_time': today.replace(hour=15, minute=0),
            'end_time': today.replace(hour=15, minute=30),
            'description': '',
            'location': 'Zoom',
            'attendees': 3,
            'recurring': False
        },
        
        # Meetings with Agenda
        {
            'id': 'mock_event_6',
            'summary': 'Sprint Planning Sprint 4',
            'start_time': today.replace(hour=11, minute=0),
            'end_time': today.replace(hour=12, minute=30),
            'description': 'Sprint 4 planning session. Review backlog, estimate user stories, assign tasks. Focus areas: user authentication, payment integration, mobile responsiveness. Bring story point estimates.',
            'location': 'Conference Room B',
            'attendees': 10,
            'recurring': False
        },
        {
            'id': 'mock_event_7',
            'summary': 'Product Demo Meeting',
            'start_time': today.replace(hour=16, minute=0),
            'end_time': today.replace(hour=17, minute=0),
            'description': 'Internal product demo and feature discussion. Review latest UI changes, discuss user feedback, plan next iteration. Demo new search functionality and performance improvements.',
            'location': 'Main Conference Room',
            'attendees': 15,
            'recurring': False
        },
        
        # Meetings without Agenda
        {
            'id': 'mock_event_8',
            'summary': 'Catch up call',
            'start_time': today.replace(hour=13, minute=0),
            'end_time': today.replace(hour=13, minute=30),
            'description': '',
            'location': 'Phone',
            'attendees': 2,
            'recurring': False
        },
        {
            'id': 'mock_event_9',
            'summary': 'Team coffee chat',
            'start_time': today.replace(hour=17, minute=30),
            'end_time': today.replace(hour=18, minute=0),
            'description': '',
            'location': 'Office Kitchen',
            'attendees': 5,
            'recurring': False
        }
    ]
    
    return mock_events

def get_mock_summary():
    """Generate a realistic AI-style summary for demo"""
    return "Busy day with 8 meetings including client demo and sprint planning. Key focus: Syncup presentation and Sprint 4 preparation."

def get_rule_based_summary():
    """Generate a simple rule-based summary"""
    events = get_mock_events()
    total = len(events)
    recurring = len([e for e in events if e['recurring']])
    new = total - recurring
    with_agenda = len([e for e in events if e['description'].strip()])
    
    return f"You have {total} meetings today. {recurring} are recurring, {new} are new. {with_agenda} meetings have detailed agendas."