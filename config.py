from dotenv import load_dotenv
load_dotenv()
import os

db_url = os.environ.get("DB_URL")
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')