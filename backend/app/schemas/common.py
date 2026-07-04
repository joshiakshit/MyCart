from decimal import Decimal

from pydantic import BaseModel


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int | None = None


class PlatformPrice(BaseModel):
    platform: str
    price: Decimal
    mrp: Decimal | None = None
    discount_pct: Decimal | None = None
    in_stock: bool = True
    delivery_eta_minutes: int | None = None
    platform_product_id: str


class PlatformProduct(BaseModel):
    platform: str
    platform_product_id: str
    name: str
    brand: str | None = None
    category: str | None = None
    unit_quantity: str | None = None
    image_url: str | None = None
    price: Decimal
    mrp: Decimal | None = None
    discount_pct: Decimal | None = None
    in_stock: bool = True
    delivery_eta_minutes: int | None = None


class ComparedProduct(BaseModel):
    name: str
    brand: str | None = None
    unit_quantity: str | None = None
    image_url: str | None = None
    prices: list[PlatformPrice]
    best_price: PlatformPrice | None = None


class PlatformStatus(BaseModel):
    status: str
    response_time_ms: int | None = None
    message: str | None = None


class SearchResponse(BaseModel):
    query: str
    results: list[ComparedProduct]
    platform_status: dict[str, PlatformStatus]
