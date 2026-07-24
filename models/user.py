from datetime import datetime
from enum import StrEnum

from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from extension import db


class Role(StrEnum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(db.Model):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(40), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    customer_profiles: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile", back_populates="User"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self):
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.get_password(), password)
