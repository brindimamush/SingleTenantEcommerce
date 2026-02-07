from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Telegram E-Commerce Bot"
    VERSION: str = "0.1.0"

settings = Settings()
