import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]