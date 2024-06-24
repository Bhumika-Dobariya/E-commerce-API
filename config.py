from dotenv import load_dotenv
load_dotenv()
import os,stripe

db_url = os.environ.get("DB_URL")
stripe.api_key= os.getenv("STRIPE_SECRET_KEY")