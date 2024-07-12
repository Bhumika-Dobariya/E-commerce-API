from fastapi import FastAPI
from src.routers.user import users 
from src.routers.product import products
from src.routers.category import category
from src.routers.address import address
from src.routers.order import orders
from src.routers.cart import carts
from src.routers.payment import payments
from src.routers.review import Reviews
from src.routers.shipping import Shippings



app =FastAPI(title = "UserDetails")
app.include_router(users)
app.include_router(products)
app.include_router(category)
app.include_router(address)
app.include_router(orders)
app.include_router(carts)
app.include_router(payments)
app.include_router(Reviews)
app.include_router(Shippings)




#
