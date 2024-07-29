from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.shipping import ShippingItem,ShippingCreate
from src.models.shipping import Shipping
from typing import List
from logs.log_config import logger



Shippings = APIRouter(tags=["Shippings"])
db = Sessionlocal()



#____________create shipping______________

@Shippings.post("/create_shipping", response_model=ShippingCreate)
def create_shipping(shippings: ShippingCreate):
    logger.info("Creating a new shipping record")
    
    db_shipping = Shipping(
        address=shippings.address,
        shipping_method=shippings.shipping_method,
        shipping_cost=shippings.shipping_cost,
        carrier_name=shippings.carrier_name,
        estimated_delivery=shippings.estimated_delivery,
        tracking_number=shippings.tracking_number,
        delivery_status=shippings.delivery_status,
        notes=shippings.notes
    )
    
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    
    logger.info(f"Shipping record created successfully with ID: {db_shipping.id}")
    
    return db_shipping



#____________read shipping___________________

@Shippings.get("/read_shipping", response_model=ShippingCreate)
def get_shipping(shipping_id: str):
    logger.info(f"Fetching shipping record with ID: {shipping_id}")
    
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id, Shipping.is_active == True, Shipping.is_deleted == False).first()
    
    if db_shipping is None:
        logger.warning(f"Shipping record not found with ID: {shipping_id}")
        raise HTTPException(status_code=404, detail="Shipping record not found")
    
    logger.info(f"Shipping record fetched successfully with ID: {shipping_id}")
    
    return db_shipping



#______________get all Shippings________________

@Shippings.get("/get_all_Shippings", response_model=List[ShippingCreate])
def get_all_shipping():
    logger.info("Fetching all active and non-deleted shipping records")
    
    db_Shipping = db.query(Shipping).filter(Shipping.is_active == True, Shipping.is_deleted == False).all()
    
    if not db_Shipping:
        logger.warning("No active and non-deleted shipping records found")
        raise HTTPException(status_code=404, detail="Shipping records not found")
    
    logger.info("All shipping records fetched successfully")
    
    return db_Shipping



#_______________update shipping__________________

@Shippings.put("/update_shipping", response_model=ShippingCreate)
def update_shipping(shipping_id: str, shipping_update: ShippingCreate):
    logger.info(f"Updating shipping record with ID: {shipping_id}")
    
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    
    if db_shipping is None:
        logger.warning(f"Shipping record not found with ID: {shipping_id}")
        raise HTTPException(status_code=404, detail="Shipping record not found")
    
    for key, value in shipping_update.dict().items():
        if value is not None:
            setattr(db_shipping, key, value)
    
    db.commit()
    db.refresh(db_shipping)
    
    logger.info(f"Shipping record updated successfully with ID: {shipping_id}")
    
    return db_shipping



#_______________delete shipping_____________________

@Shippings.delete("/delete_shipping", response_model=ShippingCreate)
def delete_shipping(shipping_id: str):
    logger.info(f"Deleting shipping record with ID: {shipping_id}")
    
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    
    if db_shipping is None:
        logger.warning(f"Shipping record not found with ID: {shipping_id}")
        raise HTTPException(status_code=404, detail="Shipping record not found")
    
    db_shipping.is_deleted = True
    db_shipping.is_active = False
    db.commit()
    
    logger.info(f"Shipping record deleted successfully with ID: {shipping_id}")
    
    return {"message": "Shipping record deleted successfully"}



#_____________shippings_carrier________________

@Shippings.get("/shippings_carrier", response_model=List[ShippingCreate])
def search_by_carrier(carrier_name: str):
    logger.info(f"Searching shipping records by carrier name: {carrier_name}")
    
    db_shippings = db.query(Shipping).filter(Shipping.carrier_name == carrier_name).all()
    
    if not db_shippings:
        logger.warning(f"No shipping records found for the carrier: {carrier_name}")
        raise HTTPException(status_code=404, detail="No shipping records found for the given carrier")
    
    logger.info(f"Shipping records found for the carrier: {carrier_name}")
    
    return db_shippings



#_____________________shipping_tracking___________________

@Shippings.get("/shipping_tracking", response_model=ShippingCreate)
def track_shipping(tracking_number: str):
    logger.info(f"Tracking shipping record with tracking number: {tracking_number}")
    
    db_shipping = db.query(Shipping).filter(Shipping.tracking_number == tracking_number).first()
    
    if db_shipping is None:
        logger.warning(f"Shipping record not found with tracking number: {tracking_number}")
        raise HTTPException(status_code=404, detail="Shipping record not found")
    
    logger.info(f"Shipping record tracked successfully with tracking number: {tracking_number}")
    
    return db_shipping
