from decimal import Decimal

from pydantic import BaseModel


class PriceHistoryPoint(BaseModel):
    price: Decimal
    mrp: Decimal | None = None
    in_stock: bool
    captured_at: str


class PriceHistoryResponse(BaseModel):
    platform: str
    product_id: str
    days: int
    history: list[PriceHistoryPoint]
