import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///bhasha.db")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    JWT_SECRET = os.environ["JWT_SECRET"]
    JWT_EXPIRY_HOURS = 24
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "png", "jpg", "jpeg", "wav", "mp3", "ogg"}
    SUPPORTED_LANGUAGES = {
        "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "kn": "Kannada",
        "ml": "Malayalam", "mr": "Marathi", "bn": "Bengali", "gu": "Gujarati",
        "pa": "Punjabi", "or": "Odia", "as": "Assamese", "ur": "Urdu",
        "sa": "Sanskrit", "kok": "Konkani", "mni": "Manipuri", "ne": "Nepali",
        "brx": "Bodo", "doi": "Dogri", "mai": "Maithili", "sat": "Santali",
        "sd": "Sindhi", "ks": "Kashmiri", "en": "English"
    }
