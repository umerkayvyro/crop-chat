import os
from dotenv import load_dotenv

load_dotenv()  # Remove this in production

class Settings:
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.5))
    STREAMING = bool(os.getenv("STREAMING", True))
    pass

settings = Settings()
