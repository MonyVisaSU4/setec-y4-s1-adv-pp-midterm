from datetime import datetime
from enum import StrEnum

from sqlalchemy import Integer, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from extension import db


class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"


class RepaymentSchedule(db.Model):
    __tablename__ = "repayment_schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    loan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("loans.loan_id"), nullable=False
    )
    loan: Mapped["Loan"] = relationship("Loan", back_populates="repayment_schedule")

    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    amount_due: Mapped[float] = mapped_column(DateTime, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    paid_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
