from fastapi import FastAPI
from src.routers.user import users 
from src.routers.OTP import otps


app =FastAPI(title = "UserDetails")

app.include_router(users)
app.include_router(otps)