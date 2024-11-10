import os
from dotenv import load_dotenv

load_dotenv("./.env")

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")
AUTH_URL = os.getenv("AUTH_URL")
OTP_URL = os.getenv("OTP_URL")
RIGISTER_CHECK_REQUEST = os.getenv("RIGISTER_CHECK_REQUEST")