from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import and_, select

from extension import db
from models import RepaymentSchedule, Loan, User, CustomerProfile
from models.repayment_schedule import Status

customer = Blueprint("customer", __name__, url_prefix="/")


@customer.route("/customer/dashboard", methods=['GET'])
@login_required
def dashboard():
    user_id = User.query.filter(User.email == current_user.email).first().user_id
    customer_id = CustomerProfile.query.filter(CustomerProfile.user_id == user_id).first().customer_id
    loan = Loan.query.filter(Loan.customer_id == customer_id).first()
    repayments = RepaymentSchedule.query.filter(and_(
        RepaymentSchedule.loan_id == loan.loan_id,
        RepaymentSchedule.status == Status.PENDING
    )).all()

    loan_row = Loan.query.filter(Loan.customer_id == customer_id).all()
    my_loan_portfolio = []
    for l in loan_row:
        repays = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == l.loan_id).all()
        mlp = {
            'priciple_amount': l.amount,
            'interest_rate': l.interest_rate,
            'duration': l.tenure_month,
            'total_repayable': l.total_payable,
            'total_paid': sum(r.amount_paid for r in repays),
            'status': l.status,
            'start_date': l.start_date
        }
        my_loan_portfolio.append(mlp)

    total_borrowed = loan.total_payable if loan else 0

    remaining_balance = 0
    for r in repayments:
        remaining_balance += r.amount_due

    next_due_installment = (RepaymentSchedule.query.filter(RepaymentSchedule.status == Status.PENDING)
                            .first().amount_due)
    due_date = RepaymentSchedule.query.filter(RepaymentSchedule.status == Status.PENDING).first().due_date

    return render_template("customer/dashboard.html",
                           total_borrowed=total_borrowed,
                           remaining_balance=remaining_balance,
                           next_due_installment=next_due_installment,
                           due_date=due_date,
                           my_loan_portfolio=my_loan_portfolio,
                           id=loan.loan_id)


@customer.route("/customer/loan", methods=['GET'])
@login_required
def loan():
    logged_user = User.query.filter(User.email == current_user.email).first()
    loans = []

    if logged_user:
        customer_profile = CustomerProfile.query.filter(CustomerProfile.user_id == logged_user.user_id).first()
        if customer_profile:
            loan_rows = Loan.query.filter(Loan.customer_id == customer_profile.customer_id).all()
            for loan in loan_rows:
                repayments = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == loan.loan_id).all()
                loans.append({
                    'loan_id': loan.loan_id,
                    'amount': loan.amount,
                    'interest_rate': loan.interest_rate,
                    'tenure_month': loan.tenure_month,
                    'total_payable': loan.total_payable,
                    'total_paid': sum(r.amount_paid for r in repayments),
                    'status': loan.status,
                    'start_date': loan.start_date,
                })

    return render_template("customer/loan.html", loans=loans)


@customer.route("/customer/profile", methods=['GET'])
@login_required
def profile():
    logged_user = User.query.filter(User.email == current_user.email).first()
    customer_profile = None

    if logged_user:
        customer_profile = CustomerProfile.query.filter(CustomerProfile.user_id == logged_user.user_id).first()

    return render_template("customer/profile.html", user=logged_user, profile=customer_profile)


@customer.route("/customer/loan/schedule/<int:id>", methods=['GET'])
@login_required
def schedule(id):
    loan = Loan.query.get_or_404(id)
    repays = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == id).all()
    agreement_detail = {
        'principal_disbursed': loan.amount,
        'annual_flat_interest': loan.interest_rate,
        'tenure_duration': relativedelta(repays[0].due_date, loan.start_date).months,
        'start_date': loan.start_date,
        'status': loan.status,
        'total_repayable': loan.total_payable,
        'total_amount_paid': sum(r.amount_paid for r in repays),
        'outstanding_balance': loan.total_payable - sum(r.amount_paid for r in repays)
    }

    installments_timeline = []
    for r in repays:
        installment = {
            'due_date': r.due_date,
            'amount_due': r.amount_due,
            'amount_paid': r.amount_paid,
            'status': r.status,
            'paid_date': r.paid_date or '---'
        }
        installments_timeline.append(installment)
    return render_template("customer/schedule.html",
                           agreement_detail=agreement_detail,
                           installments_timeline=installments_timeline)
