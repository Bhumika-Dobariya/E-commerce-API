from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.cart import Cartn,CartItemBase,CartCreate,CartItemCreate,Carts,updateCart
from src.models.products import Product
from src.models.cart import Cart,CartItem
from typing import List
from datetime import datetime
import uuid
from logs.log_config import logger


carts = APIRouter(tags=["Cart"])
db = Sessionlocal()



#_________create cart_______________

@carts.post("/create_cart/")
def create_cart(user_id: str):
    logger.info("Creating cart for user_id:", user_id)
    db_cart = Cart(user_id=user_id, created_at=datetime.now())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    logger.info("Cart created successfully for user_id: ", user_id)
    return {"message": "Cart created successfully"}



#___________add_item_to_cart______________

@carts.post("/add_item_to_cart", response_model=CartItemBase)
def add_item_to_cart(cart_id: str, item: CartItemCreate):
    logger.info("Adding item to cart_id: ", cart_id)
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        logger.error("Cart not found with id: ", cart_id)
        raise HTTPException(status_code=404, detail="Cart not found")

    db_product = db.query(Product).filter(Product.id == item.product_id).first()
    if not db_product:
        logger.error("Product not found with id: ", item.product_id)
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

    logger.info("Item added to cart_id: ", cart_id)
    return CartItemBase(
        product_id=db_cart_item.product_id,
        quantity=db_cart_item.quantity,
        price=db_cart_item.price,
        total_price=db_cart_item.total_price,
        status=item.status
    )



#______________view_cart_______________

@carts.get("/view_cart", response_model=Carts)
def view_cart(cart_id: str):
    logger.info("Fetching cart with id: ", cart_id)
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        logger.error("Cart not found with id: ", cart_id)
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

    logger.info("Cart fetched with id: ", cart_id)
    return Carts(id=db_cart.id, user_id=db_cart.user_id, items=cart_items)



#____________all_carts______________

@carts.get("/all_carts", response_model=List[Carts])
def get_all_carts():
    logger.info("Fetching all active and non-deleted carts")
    db_carts = db.query(Cart).filter(Cart.is_active == True, Cart.is_deleted == False).all()
    return db_carts



#_________________update_cart_item_price_______________

@carts.put("/update_cart_item_price")
def update_cart_item_price(cart_id: str, item_id: str, new_price: float):
    logger.info("Updating price for cart_item_id:  in cart_id: ", item_id, cart_id)
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        logger.error("Cart item not found with id: ", item_id)
        raise HTTPException(status_code=404, detail="Cart item not found")

    db_cart_item.price = new_price
    db_cart_item.total_price = new_price * db_cart_item.quantity

    db.commit()
    db.refresh(db_cart_item)

    logger.info("Price updated for cart_item_id:  in cart_id: ", item_id, cart_id)
    return {"message": "Cart item price updated successfully", "cart_item": db_cart_item}



#________________update_cart_item_quantity___________________

@carts.put("/update_cart_item_quantity", response_model=CartItemBase)
def update_cart_item_quantity(cart_id: str, item_id: str, new_quantity: int):
    logger.info("Updating quantity for cart_item_id:  in cart_id: ", item_id, cart_id)
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        logger.error("Cart item not found with id: ", item_id)
        raise HTTPException(status_code=404, detail="Cart item not found")

    db_cart_item.quantity = new_quantity
    db_cart_item.total_price = db_cart_item.price * new_quantity

    db.commit()
    db.refresh(db_cart_item)

    logger.info("Quantity updated for cart_item_id:  in cart_id: ", item_id, cart_id)
    return db_cart_item



#_______________remove_cart_item_____________________

@carts.delete("/remove_cart_item")
def remove_cart_item(cart_id: str, item_id: str):
    logger.info("Removing cart_item_id: %s from cart_id: ", item_id, cart_id)
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not db_cart_item:
        logger.error("Cart item not found with id: ", item_id)
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(db_cart_item)
    db.commit()

    logger.info("Cart item removed with id:  from cart_id: ", item_id, cart_id)
    return {"message": "Cart item removed successfully", "cart_item_id": item_id}



#_______________clear_cart_________________

@carts.delete("/clear_cart")
def clear_cart(cart_id: str):
    logger.info("Clearing cart with id: ", cart_id)
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    if not db_cart_items:
        logger.error("No items found in the cart with id: ", cart_id)
        raise HTTPException(status_code=404, detail="No items found in the cart")

    for item in db_cart_items:
        db.delete(item)

    db.commit()

    logger.info("Cart cleared with id:", cart_id)
    return {"message": "Cart cleared successfully", "cart_id": cart_id}



#_______________calculate_cart_total__________________

@carts.get("/calculate_cart_total")
def calculate_cart_total(cart_id: str):
    logger.info("Calculating total for cart_id: ", cart_id)
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    if not db_cart_items:
        logger.error("No items found in the cart with id: ", cart_id)
        raise HTTPException(status_code=404, detail="No items found in the cart")

    total_price = sum(item.total_price for item in db_cart_items)
    logger.info("Total calculated for cart_id: ", cart_id)
    return {"cart_id": cart_id, "total_price": total_price}




#________________search_cart_by_user_id________________

@carts.get("/search_cart_by_user_id")
def search_cart_by_user_id(user_id: str):
    logger.info("Searching cart for user_id: ", user_id)
    db_cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.is_active == True, Cart.is_deleted == False).all()
    if not db_cart:
        logger.error("No cart found for user_id:", user_id)
        raise HTTPException(status_code=404, detail="No cart found for the given user id")
    return db_cart



