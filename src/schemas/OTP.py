from pydantic import BaseModel


class OTPRequest(BaseModel):
    email: str

class OTPVerificationRequest(BaseModel):
    email: str
    otp: str
