from fastapi import FastAPI, HTTPException, APIRouter,Depends
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.user import UserAll,PartialUser,userpass
from src.models.user import User
from src.utils.token import get_token,get_token_logging,decode_token_user_id,decode_token_uname,decode_token_password
import random
import time


pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

users = APIRouter()
db = Sessionlocal()


#_______encode token by id__________

@users.get("/encode_token")
def encode_details(id:str):
    access_token = get_token(id)
    return access_token


#_______decode token by id________

@users.get("/decode_id")
def decode_id(token:str):
    user_id = decode_token_user_id(token)
    return user_id


#________encode logging_________

@users.get("/encode_logging")
def token_logging(uname:str,password:str):
    access_token = get_token_logging(uname,password)
    return access_token


#_____decode uname________

@users.get("/decode_uname")
def decode_uname(token:str):
    user_name = decode_token_uname(token)
    return user_name

#_____decode password____

@users.get("/decode_password")
def decode_password(token:str):
    user_password = decode_token_password(token)
    return user_password


#________create user___________

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


#______get user by token________


@users.get("/get_user_by_token",response_model=UserAll)
def read_user(token:str):
    user_id = decode_token_user_id(token)
    db_user =db.query(User).filter(User.id==user_id,User.is_active==True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    return db_user


#____get all user______


@users.get("/get_all_user",response_model=list[UserAll])
def read_all_user():
    db_user =db.query(User).all()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    return db_user
 
   
#______update user by put method________

        
@users.put("/update_user",response_model=UserAll)
def update_user(token:str, usern:UserAll):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active==True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail = "user not found")
    
    db_user.first_name=usern.first_name
    db_user.last_name = usern.last_name
    db_user.user_name = usern.user_name
    db_user.password =  pwd_context.hash(usern.password)
    db_user.email = usern.email
    db_user.mob_no = usern.mob_no
    db_user.address = usern.address  
    
    db.commit()
    return db_user


#__________update user by patch method___________


@users.patch("/update_user_by_patch", response_model=UserAll)
def update_emp_patch(token: str, user: PartialUser):
    user_id = decode_token_user_id(token)

    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()

    if  db_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    for field_name, value in user.dict().items():
        if value is not None:
            setattr( db_user, field_name, value)

    db.commit()
    return  db_user



#_______delete user__________


@users.delete("/delete_user_by_token")
def delete_user(token: str):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id , User.is_active ==True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail= "users not found")
    db_user.is_active=False
    db_user.is_deleted =True
    db.commit()
    return {"message": "user deleted successfully"}


#___________reregister____________


@users.put("/reregister")
def reregister_user(token:str,user:userpass):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id).first()
  
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    
    if db_user.is_deleted is True and db_user.is_active is False:
        if pwd_context.verify(user.password,db_user.password):
           
            db_user.is_deleted = False
            db_user.is_active = True
            
            db.commit()
       
            return True
    raise HTTPException(status_code=401,detail= "invalid crediantial")



#___________logging____________


@users.get("/logging_by_token")
def logging(token:str):
    user_name = decode_token_uname(token)
    password = decode_token_password(token)
    
    db_user = db.query(User).filter(User.user_name==user_name,User.is_active ==True).first()
    
    if db_user is None:
        
        raise HTTPException(status_code=404,detail="user not found")
    
    if not pwd_context.verify(password,db_user.password):
        
        raise HTTPException(status_code=401,detail= "incorrect password")
    
    return "loging successfully"



#____________forget password_______________


@users.put("/forget_password")
def forget_password(token:str,user_newpass:str):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id , User.is_active ==True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    
    db_user.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"


#___________reset password________________


@users.put("/reset_password_by_token")
def reset_password_by_token(token:str, old_password:str, new_password:str):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id ).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if pwd_context.verify(old_password, db_user.password):
        db_user.password =pwd_context.hash(new_password) 
        db.commit()
        return {"password reset successsfuly"}
    else:
        return "old password is not matched"
    
 

     

                                                                                                     