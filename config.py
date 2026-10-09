import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

DB_NAME = os.getenv('DB_NAME')
APP_NAME = os.getenv('APP_NAME')
BUSINESS_NAME = os.getenv('BUSINESS_NAME')
APP_NICK_NAME = os.getenv('APP_NICK_NAME')
SERVER_EMAIL = os.getenv('SERVER_EMAIL')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
COMPANY_NAME = os.getenv('COMPANY_NAME')
CONTACT_NUMBER = os.getenv('CONTACT_NUMBER')
CLIENT_CONTACT_NUMBER = os.getenv('CLIENT_CONTACT_NUMBER')


