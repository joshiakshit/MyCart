from pydantic import BaseModel, Field


class LinkAccountRequest(BaseModel):
    platform: str = Field(..., pattern=r"^(blinkit|zepto)$")
    phone_number: str = Field(..., pattern=r"^\+91\d{10}$")


class LinkAccountVerify(BaseModel):
    platform: str = Field(..., pattern=r"^(blinkit|zepto)$")
    phone_number: str = Field(..., pattern=r"^\+91\d{10}$")
    otp: str = Field(..., min_length=4, max_length=6)


class AccountInfo(BaseModel):
    platform: str
    platform_user_id: str | None = None
    is_active: bool
    delivery_address_id: str | None = None
