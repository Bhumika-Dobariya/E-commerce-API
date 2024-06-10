from fastapi import FastAPI
from src.routers.user import users 
from src.routers.OTP import otps
from src.routers.product import products

app =FastAPI(title = "UserDetails")

app.include_router(users)
app.include_router(otps)
app.include_router(products)
