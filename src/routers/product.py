from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.utils.token import get_token_product,decode_token_product_id
from src.schemas.products import AllProduct
from src.models.products import Product

products = APIRouter(tags=["Products"])
db = Sessionlocal()




#_______encode token by id__________

@products.get("/encode_token")
def encode_details(id:str):
    access_token = get_token_product(id)
    return access_token


#_______decode token by id________

@products.get("/decode_id")
def decode_id(token:str):
    user_id = decode_token_product_id(token)
    return user_id



#create product

@products.post("/create_products",response_model=AllProduct)
def create_products(product:AllProduct):
    new_product = Product(
    name  = product.name,
    description = product.description,
    price = product.price,
    stock_quantity = product.stock_quantity  
    )
    db.add(new_product)
    db.commit()
    return new_product