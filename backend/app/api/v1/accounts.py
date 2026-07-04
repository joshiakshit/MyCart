from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.account import LinkAccountRequest, LinkAccountVerify

router = APIRouter()


@router.post("/link")
async def link_account(body: LinkAccountRequest, db: AsyncSession = Depends(get_db)):
    # TODO: trigger OTP on the target platform via adapter
    return {
        "message": f"OTP requested on {body.platform}",
        "phone_number": body.phone_number,
    }


@router.post("/verify-otp")
async def verify_link_otp(body: LinkAccountVerify, db: AsyncSession = Depends(get_db)):
    # TODO: verify OTP via adapter, store encrypted tokens
    return {"message": f"{body.platform} account linked successfully"}


@router.get("")
async def list_accounts(db: AsyncSession = Depends(get_db)):
    # TODO: return linked accounts for current user
    return {"accounts": []}


@router.delete("/{platform}")
async def unlink_account(platform: str, db: AsyncSession = Depends(get_db)):
    # TODO: remove platform tokens
    return {"message": f"{platform} account unlinked"}
