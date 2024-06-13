from fastapi import FastAPI
from src.routers.UserAuthantication import users 
from src.routers.product import products
from src.routers.category import category
from src.routers.address import address
from src.routers.order import orders



app =FastAPI(title = "UserDetails")
app.include_router(users)
app.include_router(products)
app.include_router(category)
app.include_router(address)
app.include_router(orders)