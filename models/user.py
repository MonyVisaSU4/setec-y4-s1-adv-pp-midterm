from datetime import datetime
from enum import StrEnum

from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash

from extension import db


class Role(StrEnum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # This field is about login if it false user can't login.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    customer_profiles: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile",
        back_populates="user",
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = password

    def get_password(self):
        return self.password_hash

    def to_dict(self, include_profile=False):
        data = {
            'user_id': self.user_id,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            # deliberately excluding password_hash
        }
        if include_profile and self.customer_profiles:
            data['customer_profile'] = self.customer_profiles.to_dict()
        return data

    def check_password(self, password):
        return check_password_hash(self.get_password(), password)
