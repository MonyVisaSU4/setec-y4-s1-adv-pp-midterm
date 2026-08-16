from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from models import RepaymentSchedule, Loan, User, CustomerProfile
from models.repayment_schedule import Status as Status_Repay

customer = Blueprint("customer", __name__, url_prefix="/")


@customer.route("/customer/dashboard", methods=['GET'])
@login_required
def dashboard():
    # BUG FIX 1: Safely retrieve current user and associated CustomerProfile without assuming they exist.
    # Previously, `.first().user_id` and `.first().customer_id` caused AttributeError crashes on missing profiles.
    user = User.query.filter(User.email == current_user.email).first()
    if not user:
        return redirect(url_for('root'))

    customer_profile = CustomerProfile.query.filter(CustomerProfile.user_id == user.user_id).first()
    if not customer_profile:
        return render_template(
            "customer/dashboard.html",
            total_borrowed=0,
            remaining_balance=0,
            next_due_installment=0,
            due_date=None,
            my_loan_portfolio=[],
            id=None
        )

    customer_id = customer_profile.customer_id
    loan_rows = Loan.query.filter(Loan.customer_id == customer_id).all()

    my_loan_portfolio = []
    total_borrowed = 0
    remaining_balance = 0

    for l in loan_rows:
        repays = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == l.loan_id).all()
        paid_amount = sum(r.amount_paid for r in repays)
        mlp = {
            'loan_id': l.loan_id,
            'priciple_amount': l.amount,
            'interest_rate': l.interest_rate,
            'duration': l.tenure_month,
            'total_repayable': l.total_payable,
            'total_paid': paid_amount,
            'status': l.status,
            'start_date': l.start_date
        }
        my_loan_portfolio.append(mlp)
        if l.status == "active":
            total_borrowed += l.amount

    # BUG FIX 2: Previously, RepaymentSchedule.query.filter(RepaymentSchedule.status == Status.PENDING)
    # used `status` (a Python @property, not a mapped SQL column) without filtering by the customer's loans.
    # This queried the global table and crashed on `.first().amount_due` when empty.
    # Fixed to filter by customer's loan IDs and use `_status != Status_Repay.PAID`.
    loan_ids = [l.loan_id for l in loan_rows]
    next_installment = None

    if loan_ids:
        unpaid_repays = (
            RepaymentSchedule.query
            .filter(
                RepaymentSchedule.loan_id.in_(loan_ids),
                RepaymentSchedule._status != Status_Repay.PAID
            )
            .order_by(RepaymentSchedule.due_date.asc())
            .all()
        )
        remaining_balance = sum(r.amount_due - r.amount_paid for r in unpaid_repays)
        if unpaid_repays:
            next_installment = unpaid_repays[0]

    next_due_installment = next_installment.amount_due if next_installment else 0
    due_date = next_installment.due_date if next_installment else None
    first_loan_id = loan_rows[0].loan_id if loan_rows else None

    return render_template(
        "customer/dashboard.html",
        total_borrowed=total_borrowed,
        remaining_balance=remaining_balance,
        next_due_installment=next_due_installment,
        due_date=due_date,
        my_loan_portfolio=my_loan_portfolio,
        id=first_loan_id
    )


@customer.route("/customer/loan", methods=['GET'])
@login_required
def loan():
    logged_user = User.query.filter(User.email == current_user.email).first()
    loans = []

    if logged_user:
        customer_profile = CustomerProfile.query.filter(CustomerProfile.user_id == logged_user.user_id).first()
        if customer_profile:
            loan_rows = Loan.query.filter(Loan.customer_id == customer_profile.customer_id).all()
            for loan_item in loan_rows:
                repayments = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == loan_item.loan_id).all()
                loans.append({
                    'loan_id': loan_item.loan_id,
                    'amount': loan_item.amount,
                    'interest_rate': loan_item.interest_rate,
                    'tenure_month': loan_item.tenure_month,
                    'total_payable': loan_item.total_payable,
                    'total_paid': sum(r.amount_paid for r in repayments),
                    'status': loan_item.status,
                    'start_date': loan_item.start_date,
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
    loan_record = Loan.query.get_or_404(id)
    repays = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == id).order_by(RepaymentSchedule.due_date.asc()).all()

    # BUG FIX 3: Previously `relativedelta(repays[0].due_date, loan.start_date).months` crashed with IndexError
    # if `repays` was empty, and returned `1` instead of total months.
    # Fixed to use `loan_record.tenure_month` which accurately represents the full agreement tenure.
    total_paid = sum(r.amount_paid for r in repays)
    agreement_detail = {
        'principal_disbursed': loan_record.amount,
        'annual_flat_interest': loan_record.interest_rate,
        'tenure_duration': loan_record.tenure_month,
        'start_date': loan_record.start_date,
        'status': loan_record.status,
        'total_repayable': loan_record.total_payable,
        'total_amount_paid': total_paid,
        'outstanding_balance': max(0, loan_record.total_payable - total_paid)
    }

    installments_timeline = []
    for r in repays:
        installment = {
            'due_date': r.due_date,
            'amount_due': r.amount_due,
            'amount_paid': r.amount_paid,
            'status': r.status,
            'paid_date': r.paid_date.strftime('%Y-%m-%d') if r.paid_date else '---'
        }
        installments_timeline.append(installment)

    return render_template(
        "customer/schedule.html",
        agreement_detail=agreement_detail,
        installments_timeline=installments_timeline
    )
