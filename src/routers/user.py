from fastapi import FastAPI, HTTPException, APIRouter,Depends
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.user import UserAll,PartialUser
from src.models.user import User
from src.utils.token import get_token,get_token_logging,decode_token_user_id


pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

users = APIRouter()
db = Sessionlocal()


@users.get("/encode_token")
def encode_details(id:str):
    access_token = get_token(id)
    return access_token


#****encode logging*****

@users.get("/encode_logging")
def token_logging(uname:str,password:str):
    access_token = get_token_logging(uname,password)
    return access_token

#create user

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


@users.get("/get_user_by_token",response_model=UserAll)
def read_user(token:str):
    user_id = decode_token_user_id(token)
    db_user =db.query(User).filter(User.id==user_id,User.is_active==True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    return db_user


@users.get("/get_all_user",response_model=list[UserAll])
def read_all_user():
    db_user =db.query(User).all()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    return db_user
 
        
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


@users.put("/forget_password")
def forget_password(token:str,user_newpass:str):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id , User.is_active ==True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail ="user not found")
    
    db_user.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"

