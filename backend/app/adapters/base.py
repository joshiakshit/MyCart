from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.schemas.common import AuthTokens, PlatformProduct


@dataclass
class PlatformInfo:
    name: str
    display_name: str
    base_url: str
    package_name: str


class PlatformAdapter(ABC):
    info: PlatformInfo

    @abstractmethod
    async def request_otp(self, phone_number: str) -> dict:
        ...

    @abstractmethod
    async def verify_otp(self, phone_number: str, otp: str) -> AuthTokens:
        ...

    @abstractmethod
    async def refresh_auth(self, refresh_token: str) -> AuthTokens:
        ...

    @abstractmethod
    async def search(
        self,
        query: str,
        auth_token: str,
        lat: float,
        lng: float,
        limit: int = 20,
    ) -> list[PlatformProduct]:
        ...

    @abstractmethod
    async def get_product(
        self,
        product_id: str,
        auth_token: str,
        lat: float,
        lng: float,
    ) -> PlatformProduct:
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        ...
