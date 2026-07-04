import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import get_adapter
from app.core.security import decrypt_token, encrypt_token
from app.models.platform_account import PlatformAccount


class AccountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def start_link(self, user_id: uuid.UUID, platform: str, phone_number: str) -> dict:
        adapter = get_adapter(platform)
        result = await adapter.request_otp(phone_number)
        return result

    async def complete_link(
        self, user_id: uuid.UUID, platform: str, phone_number: str, otp: str
    ) -> PlatformAccount:
        adapter = get_adapter(platform)
        tokens = await adapter.verify_otp(phone_number, otp)

        account = PlatformAccount(
            user_id=user_id,
            platform=platform,
            encrypted_auth_token=encrypt_token(tokens.access_token),
            encrypted_refresh_token=encrypt_token(tokens.refresh_token),
            is_active=True,
        )
        self.db.add(account)
        await self.db.commit()
        return account

    async def get_accounts(self, user_id: uuid.UUID) -> list[PlatformAccount]:
        result = await self.db.execute(
            select(PlatformAccount).where(PlatformAccount.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_decrypted_token(self, user_id: uuid.UUID, platform: str) -> str | None:
        result = await self.db.execute(
            select(PlatformAccount).where(
                PlatformAccount.user_id == user_id,
                PlatformAccount.platform == platform,
                PlatformAccount.is_active.is_(True),
            )
        )
        account = result.scalar_one_or_none()
        if not account or not account.encrypted_auth_token:
            return None
        return decrypt_token(account.encrypted_auth_token)
