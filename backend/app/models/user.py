from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey


class User(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "users"

    phone_number: Mapped[str] = mapped_column(String(15), unique=True, index=True)

    platform_accounts = relationship("PlatformAccount", back_populates="user")
