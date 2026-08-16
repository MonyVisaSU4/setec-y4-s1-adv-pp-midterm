from datetime import date
from enum import StrEnum

from sqlalchemy import Integer, ForeignKey, Float, Enum, Date
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
        Integer,
        ForeignKey("loans.loan_id",
                   ondelete='CASCADE',
                   onupdate='CASCADE'),
        nullable=False
    )
    loan: Mapped["Loan"] = relationship("Loan", back_populates="repayment_schedule")

    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount_due: Mapped[float] = mapped_column(Float, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Float, nullable=False)
    _status: Mapped[Status] = mapped_column("status", Enum(Status), nullable=False)
    paid_date: Mapped[date] = mapped_column(Date, nullable=True)

    @property
    def status(self):
        if self.due_date < date.today() and self._status != Status.PAID:
            return Status.OVERDUE
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def to_dict(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'amount_due': self.amount_due,
            'amount_paid': self.amount_paid,
            'status': self.status.value,  # uses the @property, so OVERDUE logic applies
            'paid_date': self.paid_date.isoformat() if self.paid_date else None,
        }
