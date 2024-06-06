from fastapi import FastAPI
from src.routers.user import users 

app =FastAPI(title = "UserDetails")
app.include_router(users)