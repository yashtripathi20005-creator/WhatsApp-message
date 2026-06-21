"""
Message handler module for loading and managing scheduled messages
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self, messages_file: str = 'messages.json'):
        self.messages_file = messages_file
        self.messages = []
        self.load_messages()
    
    def load_messages(self) -> None:
        """Load messages from JSON file"""
        try:
            if os.path.exists(self.messages_file):
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
                logger.info(f"Loaded {len(self.messages)} messages from {self.messages_file}")
            else:
                # Create default messages file if it doesn't exist
                self.create_default_messages()
        except Exception as e:
            logger.error(f"Error loading messages: {e}")
            self.messages = []
    
    def create_default_messages(self) -> None:
        """Create a default messages.json file"""
        default_messages = [
            {
                "id": 1,
                "phone_number": "+1234567890",  # Replace with actual number
                "message": "Good morning! This is an automated WhatsApp message.",
                "scheduled_time": "09:00",
                "scheduled_day": "Monday",
                "active": True,
                "sent": False,
                "last_sent": None
            },
            {
                "id": 2,
                "phone_number": "+1234567890",
                "message": "Don't forget our meeting at 3 PM today!",
                "scheduled_time": "14:00",
                "scheduled_day": "Tuesday",
                "active": True,
                "sent": False,
                "last_sent": None
            }
        ]
        
        with open(self.messages_file, 'w', encoding='utf-8') as f:
            json.dump(default_messages, f, indent=4, ensure_ascii=False)
        
        self.messages = default_messages
        logger.info(f"Created default messages file: {self.messages_file}")
    
    def save_messages(self) -> None:
        """Save messages to JSON file"""
        try:
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=4, ensure_ascii=False)
            logger.info("Messages saved successfully")
        except Exception as e:
            logger.error(f"Error saving messages: {e}")
    
    def get_due_messages(self) -> List[Dict]:
        """Get messages that are due to be sent"""
        current_time = datetime.now().strftime('%H:%M')
        current_day = datetime.now().strftime('%A')
        
        due_messages = []
        for msg in self.messages:
            if (msg['active'] and 
                not msg['sent'] and 
                msg['scheduled_time'] == current_time and 
                msg['scheduled_day'] == current_day):
                due_messages.append(msg)
        
        return due_messages
    
    def mark_as_sent(self, message_id: int) -> None:
        """Mark a message as sent"""
        for msg in self.messages:
            if msg['id'] == message_id:
                msg['sent'] = True
                msg['last_sent'] = datetime.now().isoformat()
                self.save_messages()
                break
    
    def add_message(self, phone_number: str, message: str, 
                   scheduled_time: str, scheduled_day: str) -> Dict:
        """Add a new scheduled message"""
        new_id = max([m['id'] for m in self.messages]) + 1 if self.messages else 1
        
        new_message = {
            "id": new_id,
            "phone_number": phone_number,
            "message": message,
            "scheduled_time": scheduled_time,
            "scheduled_day": scheduled_day,
            "active": True,
            "sent": False,
            "last_sent": None
        }
        
        self.messages.append(new_message)
        self.save_messages()
        return new_message
    
    def delete_message(self, message_id: int) -> bool:
        """Delete a scheduled message"""
        for i, msg in enumerate(self.messages):
            if msg['id'] == message_id:
                del self.messages[i]
                self.save_messages()
                return True
        return False
    
    def get_all_messages(self) -> List[Dict]:
        """Get all messages"""
        return self.messages
