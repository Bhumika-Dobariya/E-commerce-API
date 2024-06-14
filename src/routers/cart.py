from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.cart import AllCart,UpdateCart
from src.models.products import Product
from src.models.cart import Cart
import uuid 

carts = APIRouter(tags=["Cart"])
db = Sessionlocal()



#create cart

@carts.post("/create_cart",response_model=AllCart)
def create_cart(cart_data : AllCart):
    product = db.query(Product).filter(Product.id==cart_data.product_id).first()
    if product is None:
        raise HTTPException(status_code=404,detail= "product not found")
    
    total_price = cart_data.quantity*product.price
    
    new_cart = Cart(
        id=str(uuid.uuid4()),
        user_id=cart_data.user_id,
        product_id=cart_data.product_id,
        quantity=cart_data.quantity,
        price=product.price,
        total_price=total_price,
    )
    db.add(new_cart)
    db.commit()
    return new_cart



#get cart

@carts.get("/get_cart",response_model=AllCart)
def get_category(id:str):
    db_cart= db.query(Cart).filter(Cart.id==id,Cart.is_active==True,Cart.is_deleted==False).first()
    if db_cart is None:
        raise HTTPException(status_code=404,detail="cart not found")
    return db_cart




#get all cart

@carts.get("/get_all_cart",response_model=list[AllCart])
def get_all_cart():
    db_cart = db.query(Cart).filter(Cart.is_active==True,Cart.is_deleted==False).all()
    if db_cart is None:
        raise HTTPException(status_code=404,detail ="cart not found")
    return db_cart




#update cart

@carts.patch("/update_cart", response_model=AllCart)
def update_cart(categorys: UpdateCart,id:str):
    
    db_cart= db.query(Cart).filter(Cart.id == id, Cart.is_active == True,Cart.is_deleted==False).first()

    if  db_cart is None:
        raise HTTPException(status_code=404, detail="cart  not found")

    for field_name, value in categorys.dict().items():
        if value is not None:
            setattr( db_cart, field_name, value)

    db.commit()
    return  db_cart



#delete cart

@carts.delete("/delete_cart")
def delete_cart(id:str):
    db_cart= db.query(Cart).filter(Cart.id==id,Cart.is_active==True,Cart.is_deleted==False).first()
    if db_cart is None:
        raise HTTPException(status_code=404,detail="cart not found")
    db_cart.is_active=False
    db_cart.is_deleted =True
    db.commit()
    return {"message": "cart deleted successfully"}


#get cart by user id

@carts.get("/search_cart_by_user_id")
def read_products_by_category(user_id: str):
    db_cart = db.query(Cart).filter(Cart.user_id== user_id,Cart.is_active==True,Cart.is_deleted==False).all()
    if not db_cart:
        raise HTTPException(status_code=404, detail="No cart found for the given user id")
    return db_cart