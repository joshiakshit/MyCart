import httpx

from app.adapters.base import PlatformAdapter, PlatformInfo
from app.schemas.common import AuthTokens, PlatformProduct


class BlinkitAdapter(PlatformAdapter):
    info = PlatformInfo(
        name="blinkit",
        display_name="Blinkit",
        base_url="",  # TODO: fill after reverse engineering
        package_name="com.grofers.customerapp",
    )

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=15.0)

    async def request_otp(self, phone_number: str) -> dict:
        # TODO: implement after RE — POST to Blinkit's OTP endpoint
        raise NotImplementedError("Blinkit API endpoints not yet discovered")

    async def verify_otp(self, phone_number: str, otp: str) -> AuthTokens:
        raise NotImplementedError("Blinkit API endpoints not yet discovered")

    async def refresh_auth(self, refresh_token: str) -> AuthTokens:
        raise NotImplementedError("Blinkit API endpoints not yet discovered")

    async def search(
        self,
        query: str,
        auth_token: str,
        lat: float,
        lng: float,
        limit: int = 20,
    ) -> list[PlatformProduct]:
        raise NotImplementedError("Blinkit API endpoints not yet discovered")

    async def get_product(
        self,
        product_id: str,
        auth_token: str,
        lat: float,
        lng: float,
    ) -> PlatformProduct:
        raise NotImplementedError("Blinkit API endpoints not yet discovered")

    async def health_check(self) -> bool:
        return False
