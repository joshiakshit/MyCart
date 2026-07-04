from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.auth import OTPRequest, OTPVerify, TokenResponse

router = APIRouter()


@router.post("/request-otp")
async def request_otp(body: OTPRequest, db: AsyncSession = Depends(get_db)):
    # TODO: integrate OTP provider (MSG91 / Twilio)
    return {"message": "OTP sent", "phone_number": body.phone_number}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(body: OTPVerify, db: AsyncSession = Depends(get_db)):
    # TODO: verify OTP and issue JWT
    return TokenResponse(
        access_token="placeholder",
        refresh_token="placeholder",
        token_type="bearer",
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token():
    # TODO: validate refresh token and reissue
    return TokenResponse(
        access_token="placeholder",
        refresh_token="placeholder",
        token_type="bearer",
    )
