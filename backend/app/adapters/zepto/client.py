import httpx

from app.adapters.base import PlatformAdapter, PlatformInfo
from app.schemas.common import AuthTokens, PlatformProduct


class ZeptoAdapter(PlatformAdapter):
    info = PlatformInfo(
        name="zepto",
        display_name="Zepto",
        base_url="",  # TODO: fill after reverse engineering
        package_name="com.zeptoconsumerapp",
    )

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=15.0)

    async def request_otp(self, phone_number: str) -> dict:
        raise NotImplementedError("Zepto API endpoints not yet discovered")

    async def verify_otp(self, phone_number: str, otp: str) -> AuthTokens:
        raise NotImplementedError("Zepto API endpoints not yet discovered")

    async def refresh_auth(self, refresh_token: str) -> AuthTokens:
        raise NotImplementedError("Zepto API endpoints not yet discovered")

    async def search(
        self,
        query: str,
        auth_token: str,
        lat: float,
        lng: float,
        limit: int = 20,
    ) -> list[PlatformProduct]:
        raise NotImplementedError("Zepto API endpoints not yet discovered")

    async def get_product(
        self,
        product_id: str,
        auth_token: str,
        lat: float,
        lng: float,
    ) -> PlatformProduct:
        raise NotImplementedError("Zepto API endpoints not yet discovered")

    async def health_check(self) -> bool:
        return False
