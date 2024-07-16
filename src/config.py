import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
SERVER_HOST = os.getenv("SERVER_HOST")