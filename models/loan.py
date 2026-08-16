from datetime import datetime, date
from enum import StrEnum

from sqlalchemy import Integer, ForeignKey, Float, Enum, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extension import db


class Status(StrEnum):
    ACTIVE = "active"
    CLOSED = "closed"


class Loan(db.Model):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customer_profiles.customer_id",
                   ondelete='CASCADE',
                   onupdate='CASCADE'),
        nullable=False
    )
    customer_profiles: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile", back_populates="loan"
    )

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    interest_rate: Mapped[float] = mapped_column(Float, nullable=False)
    tenure_month: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(
        Date, nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    total_payable: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    repayment_schedule: Mapped[list["RepaymentSchedule"]] = relationship(
        "RepaymentSchedule",
        back_populates="loan",
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def to_dict(self, include_repayments=False):
        data = {
            'loan_id': self.loan_id,
            'customer_id': self.customer_id,
            'amount': self.amount,
            'interest_rate': self.interest_rate,
            'tenure_month': self.tenure_month,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'status': self.status.value,
            'total_payable': self.total_payable,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_repayments:
            data['repayment_schedule'] = [r.to_dict() for r in self.repayment_schedule]
        return data
