from fastapi import FastAPI, HTTPException, APIRouter,Depends,Header
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.UserAuthantication import UserAll,PartialUser
from src.models.UserAuthantication import User
from src.models.OTP import OTPS
from src.schemas.OTP import OTPRequest, OTPVerificationRequest

from src.utils.token import decode_token_user_id,get_token
import random
from datetime import datetime, timedelta
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


users = APIRouter(tags=["UserAuthantication"])
db = Sessionlocal()



#_______________create user___________________


@users.post("/create_user",response_model=UserAll)
def create_user(user:UserAll):
   new_user = User(
       first_name = user.first_name,
       last_name = user.last_name,
       user_name = user.user_name,
       password = pwd_context.hash(user.password),
       email  = user.email,
       mob_no = user.mob_no,
       address = user.address  
   )
   db.add(new_user)
   db.commit()
   return new_user


#_________________generate and verify otp_______________________


def generate_otp(user_id: str):
    otp_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=10)

    otp = OTPS(
        id =str(uuid.uuid4()),
        user_email=user_id,
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
    message_text = f"Your OTP is {otp_code} which is valid for 10 minutes"

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

@users.post("/generate_otp")
def generate_otp_endpoint(request: OTPRequest):
    user_email = request.email 
    user_info = db.query(User).filter(User.email == user_email,User.is_active==True,User.is_deleted == False).first()
    if not user_info:
        raise HTTPException(status_code=400, detail="Invalid or missing email address")
    
    otp_code = generate_otp(user_email)
    send_otp_email(user_email, otp_code)
    return {"message": "OTP generated and sent successfully to the provided email address."}


#verify otp

@users.post("/verify_otp")
def verify_otp_endpoint(request: OTPVerificationRequest):
    email = request.email
    entered_otp = request.otp

    stored_otp = db.query(OTPS).filter(OTPS.user_email == email, OTPS.is_active == True,User.is_deleted == False).first()

    if stored_otp:
        if datetime.now() < stored_otp.expiration_time:
            if entered_otp == stored_otp.otp:

                stored_otp.is_active = False
                stored_otp.is_deleted = True
                db.commit()

                user = db.query(User).filter(User.email == email,User.is_active==True,User.is_deleted == False).first()
                if user:
                    user.is_verified = True
                    db.commit()
                    return {"message": "OTP verification successful"}
                
                if not user.is_verified:
                    user.is_verified = False
                    return {"error": "User is not verified"}
                       
            else:
                return {"error": "Incorrect OTP entered"}
        else:
            stored_otp.is_active = False
            stored_otp.is_deleted = True

            db.commit()
            return {"error": "OTP has expired" }
    else:
        return {"error": "No OTP record found for the user"}




#__________________logging____________________


@users.get("/logging")
def logging(uname: str, password: str):
    db_user = db.query(User).filter(User.user_name == uname,User.is_active == True,User.is_verified == True,User.is_deleted == False ).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(password,db_user.password):
        raise HTTPException(status_code=401,detail= "incorrect password")
    
    access_token = get_token(db_user.id)  
    return access_token



#_______________get user by token___________________


@users.get("/get_user_by_token",response_model=UserAll)
def read_user(token = Header(...)):
    user_id = decode_token_user_id(token)
    db_user =db.query(User).filter(User.id==user_id,User.is_active==True,User.is_verified==True,User.is_deleted==False).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    return db_user



#___________get all user______________

@users.get("/get_all_user",response_model=list[UserAll])
def read_all_user():
    db_user =db.query(User).filter(User.is_active == True, User.is_verified==True,User.is_deleted== False).all()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    return db_user


#______________update by put______________

@users.put("/update_user_by_put", response_model=UserAll)
def update_user(usern: UserAll, token: str = Header(...)):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not db_user.is_verified:
        return "User not verified"
    
    db_user.first_name = usern.first_name
    db_user.last_name = usern.last_name
    db_user.user_name = usern.user_name
    db_user.password = pwd_context.hash(usern.password)
    db_user.email = usern.email
    db_user.mob_no = usern.mob_no
    db_user.address = usern.address

    db.commit()
    return db_user



#_________update by patch______________

@users.patch("/update_user_by_patch", response_model=UserAll)
def update_emp_patch(user: PartialUser,token = Header(...)):
    user_id = decode_token_user_id(token)

    db_user = db.query(User).filter(User.id == user_id, User.is_active == True,User.is_verified == True,User.is_deleted==False).first()

    if  db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    if not db_user.is_verified:
        return "User not verified"

    for field_name, value in user.dict().items():
        if value is not None:
            setattr( db_user, field_name, value)

    db.commit()
    return  db_user


#_______delete user__________

@users.delete("/delete_user_by_token")
def delete_user(token = Header(...)):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id ,User.is_active ==True,User.is_verified == True,User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail= "users not found")
    
    if not db_user.is_verified:
        return "User not verified"
    
    db_user.is_active=False
    db_user.is_deleted =True
    db.commit()
    return {"message": "user deleted successfully"}

    

#___________forget password______________

@users.put("/forget_password")
def forget_password(user_newpass: str, token: str = Header(...)):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not db_user.is_verified:
        return "User not verified"
    
    db_user.password = pwd_context.hash(user_newpass)
    db.commit()
    return "Forget Password successfully"
   
   
   
#___________reset password________________


@users.put("/reset_password")
def reset_password_by_token(old_password: str, new_password: str, token: str = Header(...)):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not db_user.is_verified:
        return "User not verified"
    
    if pwd_context.verify(old_password, db_user.password):
        db_user.password = pwd_context.hash(new_password)
        db.commit()
        return {"password reset successsfuly"}
    else:
        return "old password is not matched"







