from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DB_PORT=os.getenv('DB_PORT')
SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')
RESTART_TIME_SECONDS=int(os.getenv('RESTART_TIME_SECONDS', 5))

# telegram bot parameters
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
# redis
REDIS_HOST = os.environ.get("REDIS_HOST", 'localhost')
REDIS_PORT = os.environ.get("REDIS_PORT")