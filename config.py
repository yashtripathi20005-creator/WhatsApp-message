"""
Configuration file for WhatsApp Message Scheduler
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # WhatsApp settings
    WHATSAPP_WEB_DRIVER_PATH = os.getenv('WHATSAPP_WEB_DRIVER_PATH', None)
    WHATSAPP_WAIT_TIME = int(os.getenv('WHATSAPP_WAIT_TIME', 30))
    
    # Chrome options (for running in headless mode if needed)
    CHROME_OPTIONS = [
        '--disable-gpu',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled',
        '--window-size=1920,1080'
    ]
    
    # Message template file
    MESSAGES_FILE = 'messages.json'
    
    # Logging
    LOG_FILE = 'scheduler.log'
