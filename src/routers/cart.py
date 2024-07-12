from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.cart import Cartn,CartItemBase,CartCreate,CartItemCreate,Carts,updateCart
from src.models.products import Product
from src.models.cart import Cart,CartItem
from typing import List
from datetime import datetime
import uuid

carts = APIRouter(tags=["Cart"])
db = Sessionlocal()


#create cart

@carts.post("/create_cart/")
def create_cart( user_id: str):
    db_cart = Cart(user_id=user_id, created_at=datetime.now())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return {"message": "Cart created successfully"}



@carts.post("/add_item_to_cart", response_model=CartItemBase)
def add_item_to_cart(cart_id: str, item: CartItemCreate):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db_product = db.query(Product).filter(Product.id == item.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = item.quantity * db_product.discount_price

    db_cart_item = CartItem(
        cart_id=cart_id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=db_product.discount_price,
        total_price=total_price, 
        status=item.status
        
    )

    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)

    db_cart.modified_at = datetime.utcnow()
    db.commit()

    db.refresh(db_cart)

    return CartItemBase(
        product_id=db_cart_item.product_id,
        quantity=db_cart_item.quantity,
        price=db_cart_item.price,
        total_price=db_cart_item.total_price,
         status=item.status
    )


#view cart

@carts.get("/view_cart", response_model=Carts)
def view_cart(cart_id: str):
   
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

   
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

  
    cart_items = []
    for item in db_cart_items:
        cart_item = CartItemBase(
            id=str(uuid.uuid4()),
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            total_price=item.total_price,
            status=item.status
            
        )
        cart_items.append(cart_item)

    return Carts(id=db_cart.id, user_id=db_cart.user_id, items=cart_items)



#get all cart


@carts.get("/all_carts", response_model=List[Carts])
def get_all_carts():
    db_carts = db.query(Cart).filter(Cart.is_active == True, Cart.is_deleted == False).all()
    return db_carts



#update cart

@carts.put("/update_cart_item_price")
def update_cart_item_price(cart_id: str, item_id: str, new_price: float):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db_cart_item.price = new_price
    db_cart_item.total_price = new_price * db_cart_item.quantity

    db.commit()
    db.refresh(db_cart_item)

    return {"message": "Cart item price updated successfully", "cart_item": db_cart_item}


#update quantity

@carts.put("/update_cart_item_quantity", response_model=CartItemBase)
def update_cart_item_quantity(cart_id: str, item_id: str, new_quantity: int):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db_cart_item.quantity = new_quantity
    db_cart_item.total_price = db_cart_item.price * new_quantity

    db.commit()
    db.refresh(db_cart_item)

    return db_cart_item



#remove cart item

@carts.delete("/remove_cart_item")
def remove_cart_item(cart_id: str, item_id: str):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(db_cart_item)
    db.commit()

    return {"message": "Cart item removed successfully", "cart_item_id": item_id}





#clear cart

@carts.delete("/clear_cart")
def clear_cart(cart_id: str):
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    if not db_cart_items:
        raise HTTPException(status_code=404, detail="No items found in the cart")

    for item in db_cart_items:
        db.delete(item)

    db.commit()

    return {"message": "Cart cleared successfully", "cart_id": cart_id}




#remove all

@carts.delete("/remove_cart_item")
def remove_cart_item(cart_id: str, item_id: str):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(db_cart_item)
    db.commit()

    return {"message": "Cart item removed successfully", "cart_item_id": item_id}





#calculate_cart_total

@carts.get("/calculate_cart_total/{cart_id}")
def calculate_cart_total(cart_id: str):
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    if not db_cart_items:
        raise HTTPException(status_code=404, detail="No items found in the cart")

    total_price = sum(item.total_price for item in db_cart_items)
    return {"cart_id": cart_id, "total_price": total_price}



#search_cart_by_user_id

@carts.get("/search_cart_by_user_id")
def read_products_by_category(user_id: str):
    db_cart = db.query(CartItem).filter(Cart.user_id== user_id,Cart.is_active==True,Cart.is_deleted==False).all()
    if not db_cart:
        raise HTTPException(status_code=404, detail="No cart found for the given user id")
    return db_cart




