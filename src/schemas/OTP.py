from pydantic import BaseModel


class OTPRequest(BaseModel):
    user_id: str

class OTPVerificationRequest(BaseModel):
    email: str
    otp: str