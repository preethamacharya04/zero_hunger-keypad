import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "god_mode_secret")
    
    # Audio Settings
    # Run a script to find your USB Device Index if pygame defaults to the wrong one
    USB_AUDIO_DEVICE_ID = 0 
    
    # AI Settings
    OLLAMA_MODEL = "mistral"
    
    # Email Settings (For Negotiator & Hospital Alerts)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")