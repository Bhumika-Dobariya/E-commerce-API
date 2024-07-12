from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.address import AllAddress,AddressUpdate
import uuid
from src.models.address import Address


address = APIRouter(tags=["Address"])
db = Sessionlocal()


#create address

@address.post("/create_user_address",response_model=AllAddress)
def create_address(Add: AllAddress):
    existing_address = db.query(Address).filter(Address.user_id == Add.user_id,Address.is_active==True,Address.is_deleted==False).first()
    if existing_address:
        raise HTTPException(status_code=400, detail="User already has an address")

    user_address = Address(
        id=str(uuid.uuid4()),
        city=Add.city,
        state=Add.state,
        zip_code=Add.zip_code,
        user_id=Add.user_id
    )
    db.add(user_address)
    db.commit()
    return user_address
    
    
 #get address
    
@address.get("/read_address",response_model=AllAddress)
def read_address(id:str):
    db_address = db.query(Address).filter(Address.id==id,Address.is_active==True,Address.is_deleted==False).first()
    if db_address is None:
        raise HTTPException(status_code=404,detail="address not found")
    return db_address


#get all address

@address.get("/get_all_address",response_model=list[AllAddress])
def get_all_address():
    db_address = db.query(Address).filter(Address.is_active==True,Address.is_deleted==False).all()
    if db_address is None:
        raise HTTPException(status_code=404,detail="address not found")
    return db_address




#update address

@address.patch("/update_address", response_model=AllAddress)
def update_address(addr: AddressUpdate,id:str):
    
    db_address = db.query(Address).filter(Address.id == id, Address.is_active == True,Address.is_deleted==False).first()

    if  db_address is None:
        raise HTTPException(status_code=404, detail="address not found")

    for field_name, value in addr.dict().items():
        if value is not None:
            setattr( db_address, field_name, value)

    db.commit()
    return  db_address



#delete address

@address.delete("/delete_address")
def delete_address(id:str):
    db_address = db.query(Address).filter(Address.id==id,Address.is_active==True,Address.is_deleted==False).first()
    if db_address is None:
        raise HTTPException(status_code=404,detail="address not found")
    db_address.is_active=False
    db_address.is_deleted =True
    db.commit()
    return {"message": "address deleted successfully"}



#users_in_gujarat

@address.get("/users_in_gujarat", response_model=list[AllAddress])
def get_users_in_gujarat():
    users_in_gujarat = db.query(Address).filter(Address.state == "gujarat",Address.is_active==True,Address.is_deleted==False).all()
    if not users_in_gujarat:
        raise HTTPException(status_code=404, detail="No users found in Gujarat")
    return users_in_gujarat



#search_address_by_user_id

@address.get("/search_address_by_user_id")
def read_address_by_user(user_id:str):
    db_address = db.query(Address).filter(Address.user_id == user_id,Address.is_active==True,Address.is_deleted==False).all()
    if not db_address:
        raise HTTPException(status_code=404, detail="No address found for the given user")
    return db_address