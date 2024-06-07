from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.models.OTP import OTPS
from src.schemas.OTP import OTPRequest, OTPVerificationRequest
from datetime import datetime, timedelta
import uuid
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


otps = APIRouter(tags=["OTP"])
db = Sessionlocal()


def generate_otp(user_id: str) :
    otp_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=5)

    otp = OTPS(
        user_id=user_id,
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




@otps.post("/generate_otp")
def generate_otp_endpoint(request: OTPRequest):
    user_id = request.user_id  # Assuming user_id is part of the OTPRequest
    otp_code = generate_otp(user_id)
    return {"message": "OTP generated and sent successfully to the provided email address."}





@otps.post("/verify_otp")
def verify_otp_endpoint(request: OTPVerificationRequest):
    email = request.email
    otp = request.otp

    otp_record = db.query(OTPS).filter(OTPS.email == email).order_by(OTPS.created_at.desc()).first()
    if not otp_record:
        raise HTTPException(status_code=404, detail="OTP not found")

    if otp_record.expiration_time < datetime.now():
        raise HTTPException(status_code=400, detail="OTP has expired")

    if otp_record.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": "OTP verified successfully"}
