from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DB_PORT=os.getenv('DB_PORT')
SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')
RESTART_TIME_SECONDS=int(os.getenv('RESTART_TIME_SECONDS', 5))
print(f"DB_PORT: {DB_PORT}")
print(f"POSTGRES_PASSWORD: {POSTGRES_PASSWORD}")
print(f"POSTGRES_USER: {os.environ.get('DB_PORT')}")
print(f"RESTART_TIME_SECONDS: {os.environ.get('RESTART_TIME_SECONDS')}")