#!/usr/bin/env python3
"""
AI Calendar Assistant - Main Application

Fetches today's Google Calendar events and generates an AI-powered categorized summary.
"""

import sys
from datetime import datetime
from calendar_client import CalendarClient
from ai_processor import AIProcessor
from config import EMOJI_ENABLED


def print_banner():
    """Print application banner"""
    today = datetime.now().strftime('%B %d, %Y')
    print("=" * 60)
    print("🤖 AI CALENDAR ASSISTANT")
    print("=" * 60)
    print(f"📅 Today: {today}")
    print()


def format_time(dt):
    """Format datetime for display"""
    return dt.strftime('%I:%M %p').lstrip('0')


def print_event_list(events, title, emoji="📋"):
    """Print a formatted list of events"""
    if not events:
        return
    
    print(f"\n{emoji} {title.upper()} ({len(events)}):")
    print("-" * 40)
    
    for event in events:
        start_time = format_time(event['start_time'])
        end_time = format_time(event['end_time'])
        duration = event['end_time'] - event['start_time']
        duration_mins = int(duration.total_seconds() / 60)
        
        print(f"• {event['summary']}")
        print(f"  ⏰ {start_time} - {end_time} ({duration_mins} min)")
        
        if event['description']:
            # Truncate long descriptions
            desc = event['description'][:100]
            if len(event['description']) > 100:
                desc += "..."
            print(f"  📋 {desc}")
        
        if event['location']:
            print(f"  📍 {event['location']}")
        
        if event['attendees'] > 1:
            print(f"  👥 {event['attendees']} attendees")
        
        print()


def print_summary(categorization):
    """Print the complete calendar summary"""
    print_banner()
    
    # Overall summary
    print("📊 DAILY SUMMARY")
    print("-" * 40)
    print(categorization['summary'])
    print()
    
    # Recurring meetings
    if categorization['recurring_meetings']:
        print_event_list(
            categorization['recurring_meetings'], 
            "Recurring Meetings", 
            "🔄"
        )
    
    # New meetings
    if categorization['new_meetings']:
        print_event_list(
            categorization['new_meetings'], 
            "New Meetings", 
            "🆕"
        )
    
    # Meetings with agenda
    if categorization['meetings_with_agenda']:
        print_event_list(
            categorization['meetings_with_agenda'], 
            "Meetings with Agenda", 
            "📋"
        )
    
    # Meetings without agenda
    if categorization['meetings_without_agenda']:
        print_event_list(
            categorization['meetings_without_agenda'], 
            "Meetings without Agenda", 
            "❓"
        )
    
    # Statistics
    all_events = (categorization['recurring_meetings'] + 
                 categorization['new_meetings'])
    
    if all_events:
        total_duration = sum([
            (event['end_time'] - event['start_time']).total_seconds() / 3600 
            for event in all_events
        ])
        
        print("\n📈 STATISTICS")
        print("-" * 40)
        print(f"Total meetings: {len(all_events)}")
        print(f"Total time: {total_duration:.1f} hours")
        print(f"Recurring: {len(categorization['recurring_meetings'])}")
        print(f"New: {len(categorization['new_meetings'])}")
        print(f"With agenda: {len(categorization['meetings_with_agenda'])}")
        print(f"Without agenda: {len(categorization['meetings_without_agenda'])}")
    
    print("\n" + "=" * 60)
    print("✨ Have a productive day!")
    print("=" * 60)


def main():
    """Main application function"""
    try:
        print("🚀 Starting AI Calendar Assistant...")
        print()
        
        # Step 1: Initialize Calendar Client
        print("📅 Connecting to Google Calendar...")
        calendar_client = CalendarClient()
        
        if not calendar_client.authenticate():
            print("❌ Failed to connect to Google Calendar. Please check your credentials.")
            return 1
        
        # Step 2: Fetch today's events
        events = calendar_client.get_todays_events()
        
        if not events:
            print_banner()
            print("📭 No meetings scheduled for today!")
            print("🎉 Enjoy your free day!")
            return 0
        
        # Step 3: Initialize AI Processor
        print("\n🤖 Initializing AI processor...")
        ai_processor = AIProcessor()
        
        # Step 4: Categorize events
        print("🔍 Analyzing and categorizing events...")
        categorization = ai_processor.categorize_events(events)
        
        # Step 5: Display results
        print_summary(categorization)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please check your setup and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())