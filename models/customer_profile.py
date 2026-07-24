from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extension import db


class CustomerProfile(db.Model):
    __tablename__ = "customer_profiles"

    customer_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="CustomerProfile")

    loan: Mapped[list["CustomerProfile"]] = relationship(
        "Loan", back_populates="CustomerProfile"
    )

    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    national_id: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
