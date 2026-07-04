import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("platform_products.id"), index=True
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    mrp: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    discount_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    delivery_eta_minutes: Mapped[int | None] = mapped_column(Integer)
    location_lat: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    location_lng: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
