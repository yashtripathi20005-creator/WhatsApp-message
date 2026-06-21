"""
Scheduler module for managing WhatsApp message scheduling
"""
import schedule
import time
import logging
from datetime import datetime
from message_handler import MessageHandler
import pywhatkit
import sys
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppScheduler:
    def __init__(self):
        self.message_handler = MessageHandler()
        self.running = False
    
    def send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        """
        Send WhatsApp message using pywhatkit
        
        Args:
            phone_number: Phone number with country code (e.g., +1234567890)
            message: Message to send
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Remove '+' if present as pywhatkit expects number without '+'
            phone = phone_number.replace('+', '')
            
            # Get current time for scheduling
            now = datetime.now()
            hour = now.hour
            minute = now.minute + 2  # Send 2 minutes from now
            
            # If minute exceeds 60, adjust hour and minute
            if minute >= 60:
                minute = minute - 60
                hour = hour + 1
                if hour >= 24:
                    hour = 0
            
            # Send message
            logger.info(f"Sending message to {phone_number}: {message[:50]}...")
            
            # Use pywhatkit to send message
            pywhatkit.sendwhatmsg(phone, message, hour, minute)
            
            logger.info(f"Message sent successfully to {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {phone_number}: {e}")
            return False
    
    def process_due_messages(self) -> None:
        """Process all due messages"""
        logger.info("Checking for due messages...")
        due_messages = self.message_handler.get_due_messages()
        
        if not due_messages:
            logger.info("No messages due at this time")
            return
        
        logger.info(f"Found {len(due_messages)} due messages")
        
        for msg in due_messages:
            phone = msg['phone_number']
            message = msg['message']
            msg_id = msg['id']
            
            # Send message
            success = self.send_whatsapp_message(phone, message)
            
            if success:
                self.message_handler.mark_as_sent(msg_id)
                logger.info(f"Message {msg_id} marked as sent")
            else:
                logger.error(f"Failed to send message {msg_id}")
    
    def run_continuous(self) -> None:
        """Run the scheduler continuously"""
        self.running = True
        logger.info("Starting WhatsApp Scheduler...")
        logger.info("Press Ctrl+C to stop")
        
        # Schedule the job to run every minute
        schedule.every(1).minutes.do(self.process_due_messages)
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\nShutting down scheduler...")
                self.running = False
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(5)
    
    def run_one_time(self) -> None:
        """Run the scheduler once to process due messages"""
        logger.info("Running one-time check...")
        self.process_due_messages()
        logger.info("One-time check completed")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            scheduler = WhatsAppScheduler()
            scheduler.run_one_time()
        else:
            print("Usage: python scheduler.py [--once]")
            print("  --once: Run one-time check for due messages")
    else:
        # Run continuously
        scheduler = WhatsAppScheduler()
        scheduler.run_continuous()

if __name__ == "__main__":
    main()
