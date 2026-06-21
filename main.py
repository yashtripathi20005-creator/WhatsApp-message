"""
Main entry point for WhatsApp Message Scheduler
Provides CLI interface for managing scheduled messages
"""
import sys
import json
from message_handler import MessageHandler
from scheduler import WhatsAppScheduler
from datetime import datetime

def show_help():
    """Show help information"""
    print("""
WhatsApp Message Scheduler CLI
=============================
Commands:
  list                - List all scheduled messages
  add                 - Add a new scheduled message
  delete <id>         - Delete a message by ID
  run                 - Run the scheduler continuously
  run-once            - Run one-time check for due messages
  help                - Show this help message
  quit                - Exit the application

Examples:
  python main.py list
  python main.py add
  python main.py delete 1
  python main.py run
  python main.py run-once
    """)

def list_messages():
    """List all scheduled messages"""
    handler = MessageHandler()
    messages = handler.get_all_messages()
    
    if not messages:
        print("No scheduled messages found.")
        return
    
    print("\nScheduled Messages:")
    print("-" * 80)
    print(f"{'ID':<5} {'Phone':<15} {'Time':<10} {'Day':<12} {'Active':<8} {'Sent':<8} {'Message'}")
    print("-" * 80)
    
    for msg in messages:
        status = "✓" if msg['active'] else "✗"
        sent = "✓" if msg['sent'] else "✗"
        message_preview = msg['message'][:40] + "..." if len(msg['message']) > 40 else msg['message']
        print(f"{msg['id']:<5} {msg['phone_number']:<15} {msg['scheduled_time']:<10} "
              f"{msg['scheduled_day']:<12} {status:<8} {sent:<8} {message_preview}")

def add_message():
    """Add a new scheduled message"""
    handler = MessageHandler()
    
    print("\nAdd New Scheduled Message")
    print("-" * 40)
    
    phone = input("Phone number (with country code, e.g., +1234567890): ").strip()
    message = input("Message to send: ").strip()
    time = input("Scheduled time (HH:MM, 24-hour format): ").strip()
    day = input("Scheduled day (e.g., Monday, Tuesday, etc.): ").strip()
    
    # Validate inputs
    if not phone or not message or not time or not day:
        print("All fields are required!")
        return
    
    try:
        datetime.strptime(time, '%H:%M')
    except ValueError:
        print("Invalid time format. Use HH:MM in 24-hour format.")
        return
    
    # Capitalize day
    day = day.capitalize()
    
    # Add message
    new_msg = handler.add_message(phone, message, time, day)
    print(f"\nMessage {new_msg['id']} added successfully!")
    print(f"Phone: {new_msg['phone_number']}")
    print(f"Time: {new_msg['scheduled_time']}")
    print(f"Day: {new_msg['scheduled_day']}")
    print(f"Message: {new_msg['message']}")

def delete_message(msg_id: str):
    """Delete a scheduled message"""
    handler = MessageHandler()
    
    try:
        msg_id = int(msg_id)
    except ValueError:
        print("Invalid ID. Please provide a number.")
        return
    
    success = handler.delete_message(msg_id)
    if success:
        print(f"Message {msg_id} deleted successfully.")
    else:
        print(f"Message {msg_id} not found.")

def run_scheduler():
    """Run the scheduler continuously"""
    scheduler = WhatsAppScheduler()
    scheduler.run_continuous()

def run_scheduler_once():
    """Run the scheduler once"""
    scheduler = WhatsAppScheduler()
    scheduler.run_one_time()

def main():
    """Main CLI"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'help':
        show_help()
    elif command == 'list':
        list_messages()
    elif command == 'add':
        add_message()
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Please provide the message ID to delete.")
            print("Usage: python main.py delete <id>")
            return
        delete_message(sys.argv[2])
    elif command == 'run':
        run_scheduler()
    elif command == 'run-once':
        run_scheduler_once()
    elif command == 'quit' or command == 'exit':
        print("Goodbye!")
        sys.exit(0)
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
