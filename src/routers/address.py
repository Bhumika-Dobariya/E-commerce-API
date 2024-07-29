from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.address import AllAddress,AddressUpdate
import uuid
from src.models.address import Address
from logs.log_config import logger
from typing import List


address = APIRouter(tags=["Address"])
db = Sessionlocal()



#______________create user address___________________

@address.post("/create_user_address", response_model=AllAddress)
def create_address(Add: AllAddress):
    logger.info("Creating address for user_id:", Add.user_id)
    existing_address = db.query(Address).filter(Address.user_id == Add.user_id, Address.is_active == True, Address.is_deleted == False).first()
    if existing_address:
        logger.error("User with user_id: already has an address", Add.user_id)
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
    logger.info("Address created for user_id:", Add.user_id)
    return user_address



#____________read address_________________

@address.get("/read_address", response_model=AllAddress)
def read_address(id: str):
    logger.info("Fetching address with id:", id)
    db_address = db.query(Address).filter(Address.id == id, Address.is_active == True, Address.is_deleted == False).first()
    if db_address is None:
        logger.error("Address not found with id:", id)
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address



#_____________get all address________________

@address.get("/get_all_address", response_model=List[AllAddress])
def get_all_address():
    logger.info("Fetching all active and non-deleted addresses")
    db_addresses = db.query(Address).filter(Address.is_active == True, Address.is_deleted == False).all()
    if not db_addresses:
        logger.error("No addresses found")
        raise HTTPException(status_code=404, detail="Addresses not found")
    return db_addresses



#______________update address________________

@address.patch("/update_address", response_model=AllAddress)
def update_address(addr: AddressUpdate, id: str):
    logger.info("Updating address with id:", id)
    db_address = db.query(Address).filter(Address.id == id, Address.is_active == True, Address.is_deleted == False).first()

    if db_address is None:
        logger.error("Address not found with id:", id)
        raise HTTPException(status_code=404, detail="Address not found")

    for field_name, value in addr.dict().items():
        if value is not None:
            setattr(db_address, field_name, value)

    db.commit()
    logger.info("Address updated with id:", db_address.id)
    return db_address



#_____________delete address______________

@address.delete("/delete_address")
def delete_address(id: str):
    logger.info("Deleting address with id:", id)
    db_address = db.query(Address).filter(Address.id == id, Address.is_active == True, Address.is_deleted == False).first()
    if db_address is None:
        logger.error("Address not found with id:", id)
        raise HTTPException(status_code=404, detail="Address not found")
    db_address.is_active = False
    db_address.is_deleted = True
    db.commit()
    logger.info("Address deleted with id:", db_address.id)
    return {"message": "Address deleted successfully"}



#________________users in gujarat_______________

@address.get("/users_in_gujarat", response_model=List[AllAddress])
def get_users_in_gujarat():
    logger.info("Fetching users in Gujarat")
    users_in_gujarat = db.query(Address).filter(Address.state == "gujarat", Address.is_active == True, Address.is_deleted == False).all()
    if not users_in_gujarat:
        logger.error("No users found in Gujarat")
        raise HTTPException(status_code=404, detail="No users found in Gujarat")
    return users_in_gujarat



#____________search address by user id___________

@address.get("/search_address_by_user_id")
def read_address_by_user(user_id: str):
    logger.info("Fetching addresses for user_id:", user_id)
    db_address = db.query(Address).filter(Address.user_id == user_id, Address.is_active == True, Address.is_deleted == False).all()
    if not db_address:
        logger.error("No address found for user_id:", user_id)
        raise HTTPException(status_code=404, detail="No address found for the given user")
    return db_address
