from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.models.OTP import OTPS
from src.models.user import User
from src.schemas.OTP import OTPRequest, OTPVerificationRequest
from datetime import datetime, timedelta
import uuid
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


otps = APIRouter(tags=["OTP"])
db = Sessionlocal()


def generate_otp(user_email: str):
    otp_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=5)

    otp = OTPS(
        id =str(uuid.uuid4()),
        user_email=user_email,
        otp=otp_code,
        expiration_time=expiration_time
    )
    db.add(otp)
    db.commit()
    return otp_code



def send_otp_email(email: str, otp_code: str):
    sender_email = "bhumikadobariya2412@gmail.com"
    receiver_email = email
    password = "qzdjaauunsmgrvgd"
    subject = "Your OTP Code"
    message_text = f"Your OTP is {otp_code} which is valid for 5 minutes"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Mail sent successfully")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")





#generate otp


@otps.post("/generate_otp")
def generate_otp_endpoint(request: OTPRequest):
    user_email = request.email 
    user_info = db.query(User).filter(User.email == user_email).first()
    if not user_info:
        raise HTTPException(status_code=400, detail="Invalid or missing email address")
    
    otp_code = generate_otp(user_email)
    send_otp_email(user_email, otp_code)
    return {"message": "OTP generated and sent successfully to the provided email address."}




#verify otp


@otps.post("/verify_otp")
def verify_otp_endpoint(request: OTPVerificationRequest):
    email = request.email
    entered_otp = request.otp

    stored_otp = db.query(OTPS).filter(OTPS.user_email == email,OTPS.is_active == True).first()
    if stored_otp:
        if datetime.now() < stored_otp.expiration_time:
            if entered_otp == stored_otp.otp:
                return {"message": "OTP verification successful"}
            else:
                return {"error": "Incorrect OTP entered"}
        else:
            stored_otp.is_active = False
            stored_otp.is_deleted = True
            db.commit()
            return {"error": "OTP has expired" }
    else:
        return {"error": "No OTP record found for the user"}
   

  