from pydantic import BaseModel, Field


class OTPRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+91\d{10}$")


class OTPVerify(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+91\d{10}$")
    otp: str = Field(..., min_length=4, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
