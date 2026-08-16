from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    flash,
)
from flask_login import login_required
from sqlalchemy import func, select, and_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from decorators import admin_required
from extension import db
from models import Loan, User, RepaymentSchedule, CustomerProfile
from models.loan import Status as Status_Loan
from models.repayment_schedule import Status as Status_Repayment
from models.user import Role

admin = Blueprint("admin", __name__, url_prefix="/")


@admin.route("/admin/dashboard", methods=["GET"])
@admin_required
@login_required
def dashboard():
    data = {
        'total_borrower': 0,
        'active_loan': 0,
        'total_disbursed': 0,
        'total_collected': 0,
        'overdue_installment': []
    }

    try:
        data['total_borrower'] = db.session.query(func.count(CustomerProfile.customer_id)).scalar()
        data['active_loan'] = Loan.query.filter(Loan.status.like(Status_Loan.ACTIVE)).count()
        data['total_disbursed'] = db.session.query(func.sum(Loan.amount)).scalar()
        data['total_collected'] = db.session.query(func.sum(RepaymentSchedule.amount_paid)).scalar()

        repayment_query = RepaymentSchedule.query
        filter_status = repayment_query.filter(RepaymentSchedule._status == Status_Repayment.OVERDUE)
        all_repayment = filter_status.all()

        for g in all_repayment:
            customer_profile_id = Loan.query.get_or_404(g.loan_id).customer_id
            customer_profile = CustomerProfile.query.get_or_404(customer_profile_id)
            user_id = User.query.get_or_404(customer_profile.user_id)
            get_borrower_email = user_id.email

            data['overdue_installment'].append({
                'id': g.id,
                'email': get_borrower_email,
                'due_date': g.due_date,
                'amount_due': g.amount_due,
                'amount_paid': g.amount_paid
            })
    except Exception as e:
        print(e)

    return render_template(
        "admin/dashboard.html",
        overdue_installment=data['overdue_installment'],
        total_borrower=data['total_borrower'],
        active_loan=data['active_loan'],
        total_disbursed=data['total_disbursed'],
        total_collected=data['total_collected'],
    )


@admin.route("/admin/borrower", methods=["GET"])
@admin_required
@login_required
def borrower():
    res = None
    try:
        # BUG FIX: The previous join was `.join(CustomerProfile, User.user_id == CustomerProfile.user_id)`
        # which redundantly joined CustomerProfile to CustomerProfile. Fixed to join User on CustomerProfile.user_id.
        statement = select(
            CustomerProfile.customer_id,
            User.email,
            CustomerProfile.address,
            CustomerProfile.national_id,
            CustomerProfile.phone,
            CustomerProfile.created_at,
        ).join(User, CustomerProfile.user_id == User.user_id)

        borrowers = db.session.execute(statement).all()

        if len(borrowers) != 0:
            res = borrowers
    except Exception as e:
        print(e)

    return render_template("admin/borrower/borrower.html", list=res)


@admin.route("/admin/borrower/filter", methods=["GET"])
@admin_required
@login_required
def filter_borrower():
    # BUG FIX: Fixed join clause to correctly join User on CustomerProfile.user_id.
    statement = select(
        CustomerProfile.customer_id,
        User.email,
        CustomerProfile.address,
        CustomerProfile.national_id,
        CustomerProfile.phone,
        CustomerProfile.created_at,
    ).join(User, CustomerProfile.user_id == User.user_id)

    res = db.session.execute(statement).all()
    data = [dict(row._mapping) for row in res]
    return jsonify(data)


@admin.route("/admin/borrower/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_borrower():
    try:
        if request.method == "POST":
            nationality: str = request.form.get("national_id")
            phone: str = request.form.get("phone")
            address: str = request.form.get("address")
            login_email: str = request.form.get("login-email")
            login_password: str = request.form.get("login-password")

            user = User(
                email=login_email,
                password_hash=generate_password_hash(login_password),
                role=Role.CUSTOMER,
            )
            db.session.add(user)

            # INSERT has send but not yet commit.
            db.session.flush()

            borrower = CustomerProfile(
                user_id=user.user_id,
                phone=phone,
                address=address,
                national_id=nationality,
            )
            db.session.add(borrower)

            if borrower and user:
                db.session.commit()

            flash("borrower been added", "success")
    except Exception as e:
        db.session.rollback()
        print(e)
    return render_template("admin/borrower/add.html")


@admin.route("/admin/borrower/view/<int:id>", methods=["GET"])
@login_required
@admin_required
def view_borrower(id):
    userdata = None
    loandata = None

    try:
        userstmt = db.session.execute(
            select(
                CustomerProfile.customer_id,
                User.email,
                CustomerProfile.national_id,
                CustomerProfile.phone,
                CustomerProfile.address,
                CustomerProfile.created_at,
            )
            .join(CustomerProfile, User.user_id == CustomerProfile.user_id)
            .where(CustomerProfile.customer_id == id)
        ).first()

        loanstmt = db.session.execute(
            select(
                Loan.loan_id,
                Loan.amount,
                Loan.interest_rate,
                Loan.tenure_month,
                Loan.total_payable,
                Loan.status,
                Loan.start_date,
            ).where(Loan.customer_id == id)
        ).all()

        if userstmt and loanstmt is not None:
            userdata = userstmt
            loandata = [dict(row._mapping) for row in loanstmt]
    except Exception as e:
        print(e)

    return render_template("admin/borrower/view.html", id=id, data=userdata, loandata=loandata)


@admin.route("/admin/borrower/update/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def update_borrower(id):
    try:
        borrowers = CustomerProfile.query.get_or_404(id)

        if request.method == "POST":
            nationality: str = request.form["nationality"]
            phone: str = request.form["phone"]
            address: str = request.form["address"]
            password: str | None = request.form["password"]

            borrowers.national_id = nationality
            borrowers.phone = phone
            borrowers.address = address

            db.session.flush()

            if password:
                user = User.query.get_or_404(borrowers.user_id)
                user.password_hash = generate_password_hash(password)

            if borrowers:
                db.session.commit()
            flash("borrower been updated", "success")
    except Exception as e:
        db.session.rollback()
        print(e)
    return render_template("admin/borrower/edit.html", id=id, borrowers=borrowers)


@admin.route("/admin/borrower/delete/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_borrower(id):
    try:
        loan = Loan.query.filter(Loan.customer_id == id).first()

        if loan:
            # BUG FIX: Previously this returned render_template("admin/borrower/edit.html") without
            # required arguments, breaking AJAX SweetAlert callers. Returning JSON allows the
            # frontend JS handler to display the error alert gracefully.
            return jsonify({"message": "This borrower has loans. Deletion cannot be allowed."})
        borrower = CustomerProfile.query.get_or_404(id)
        user = borrower.user

        db.session.delete(borrower)
        if user:
            db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Success"})
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "This borrower has loans. Deletion cannot be allowed."})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message": f"Error deleting borrower: {str(e)}"})


@admin.route("/admin/loan", methods=["GET"])
@login_required
@admin_required
def loan():
    try:
        loans = Loan.query.all()
    except Exception as e:
        loans = None
        print(e)
    return render_template("admin/loan/loan.html", loans=loans)


@admin.route("/admin/loan/filter", methods=["GET"])
@login_required
@admin_required
def filter_loan():
    try:
        status = request.args.get("status")
        sdate = request.args.get("sdate")
        edate = request.args.get("edate")
        loans = (
            select(
                Loan.loan_id,
                User.email,
                Loan.amount,
                Loan.interest_rate,
                Loan.tenure_month,
                Loan.total_payable,
                Loan.status,
                Loan.start_date,
            )
            .join(CustomerProfile, Loan.customer_id == CustomerProfile.customer_id)
            .join(User, CustomerProfile.user_id == User.user_id)
        )

        condition = []

        if status and status != "all":
            condition.append(Loan.status == Status_Loan(status))
        if sdate:
            condition.append(Loan.start_date >= sdate)
        if edate:
            condition.append(Loan.start_date <= edate)

        res = db.session.execute(loans.filter(and_(*condition))).all()
        data = [dict(row._mapping) for row in res]
        return jsonify(data)
    except Exception as e:
        print(e)


@admin.route("/admin/loan/view/<int:id>", methods=["GET"])
@login_required
@admin_required
def view_loan(id):
    loans = Loan.query.get_or_404(id)
    repayment_schedule = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == loans.loan_id).all()

    # BUG FIX: The previous query executed an unaggregated SELECT on RepaymentSchedule.amount_paid
    # with NO WHERE clause for the loan, fetching an arbitrary first row's amount across all loans.
    # We now accurately calculate the sum of amount_paid for this specific loan's schedules.
    total_collect = sum(r.amount_paid for r in repayment_schedule)

    return render_template(
        "admin/loan/view.html",
        loans=loans,
        total_collect=total_collect,
        repayment_schedule=repayment_schedule
    )


@admin.route("/admin/loan/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_loan():
    try:
        borrowers = CustomerProfile.query.all()
        if request.method == "POST":
            borrower_choose = int(request.form["customer_id"])
            principle = float(request.form["principle-loan"])
            interest = float(request.form["interest"])
            tenure = int(request.form["tenure"])
            start_date_raw = request.form["start-date"]
            start_date = date.fromisoformat(start_date_raw) if start_date_raw else date.today()
            tenure_year = tenure / 12
            total_interest = principle * (interest / 100) * tenure_year
            total_payable = principle + total_interest

            # BUG FIX: The previous check was `findLoan = Loan.query.filter(loans.customer_id == Loan.customer_id).all()`
            # which evaluated `Loan.customer_id == Loan.customer_id` (a SQL column identity tautology 1=1).
            # This matched ALL loans in the database and blocked any new loans once any loan existed.
            # Fixed to query active loans for the selected borrower.
            findLoan = Loan.query.filter(
                Loan.customer_id == borrower_choose,
                Loan.status == Status_Loan.ACTIVE
            ).first()

            if findLoan:
                flash('This borrower already has an active loan.', 'warning')
            else:
                new_loan = Loan(
                    customer_id=borrower_choose,
                    amount=principle,
                    interest_rate=interest,
                    tenure_month=tenure,
                    start_date=start_date,
                    status=Status_Loan.ACTIVE,
                    total_payable=total_payable,
                )
                db.session.add(new_loan)
                db.session.flush()

                replayment_schedule = []

                for i in range(tenure):
                    replayment_schedule.append(
                        RepaymentSchedule(
                            loan_id=new_loan.loan_id,
                            due_date=start_date + relativedelta(months=i + 1),
                            amount_due=total_payable / tenure,
                            amount_paid=0,
                            status=Status_Repayment.PENDING,
                            paid_date=None
                        )
                    )

                for r in replayment_schedule:
                    db.session.add(r)

                db.session.commit()
                flash("loan added", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")
    return render_template("admin/loan/add.html", borrowers=borrowers)


@admin.route("/admin/report", methods=["GET"])
@login_required
@admin_required
def report():
    try:
        selected = (
            select(
                Loan.loan_id,
                User.email,
                Loan.amount,
                Loan.interest_rate,
                Loan.tenure_month,
                Loan.total_payable,
                Loan.status,
                Loan.start_date,
            )
            .join(CustomerProfile, Loan.customer_id == CustomerProfile.customer_id)
            .join(User, CustomerProfile.user_id == User.user_id)
        )

        audited_loan_records = db.session.execute(selected).all()

        # BUG FIX: matching_loan previously counted CustomerProfile.customer_id (borrowers),
        # whereas the report represents Matching Loans. Fixed to count audited matching loans.
        matching_loan = len(audited_loan_records)
        disbursed_principal = db.session.execute(select(func.sum(Loan.amount))).scalar() or 0
        total_payable = db.session.execute(select(func.sum(Loan.total_payable))).scalar() or 0
        expected_interest = (total_payable - disbursed_principal) if total_payable > disbursed_principal else 0
        collected_repayment = (
                db.session.execute(select(func.sum(RepaymentSchedule.amount_paid))).scalar() or 0
        )
    except Exception as e:
        print(e)
        audited_loan_records = []
        matching_loan = 0
        disbursed_principal = 0
        expected_interest = 0
        collected_repayment = 0

    return render_template(
        "admin/report.html",
        matching_loan=matching_loan,
        disbursed_principal=disbursed_principal,
        expected_interest=expected_interest,
        collected_repayment=collected_repayment,
        audited_loan_records=audited_loan_records,
    )


@admin.route("/admin/report/filter", methods=["GET"])
@admin_required
@login_required
def filter_report():
    try:
        report_status = request.args.get("report_status")
        report_sdate = request.args.get("report_sdate")
        report_edate = request.args.get("report_edate")
        selected = (
            select(
                Loan.loan_id,
                User.email,
                Loan.amount,
                Loan.interest_rate,
                Loan.tenure_month,
                Loan.total_payable,
                Loan.status,
                Loan.start_date,
            )
            .join(CustomerProfile, Loan.customer_id == CustomerProfile.customer_id)
            .join(User, CustomerProfile.user_id == User.user_id)
        )

        condition = []

        if report_status and report_status != "all":
            condition.append(Loan.status == Status_Loan(report_status))
        if report_sdate:
            condition.append(Loan.start_date >= report_sdate)
        if report_edate:
            condition.append(Loan.start_date <= report_edate)

        get_audited_loan_records = db.session.execute(
            selected.filter(and_(*condition))
        ).all()

        audited_loan_records = [dict(row._mapping) for row in get_audited_loan_records]
        return jsonify(audited_loan_records)
    except Exception as e:
        print(e)
        return jsonify([])


@admin.route('/admin/loan/repay/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def repay(id):
    repayment = RepaymentSchedule.query.get_or_404(id)

    if request.method == "POST":
        # BUG FIX: Parse amount as float and parse modalPayDate if submitted.
        # Also check if all installments for this loan are now paid and auto-close loan.
        amount_paid = float(request.form.get('modalRepayAmount', repayment.amount_due))
        modal_pay_date = request.form.get('modalPayDate')
        paid_date = date.fromisoformat(modal_pay_date) if modal_pay_date else date.today()

        repayment.amount_paid = amount_paid
        repayment.paid_date = paid_date
        repayment.status = Status_Repayment.PAID

        # Automatically check if loan is fully paid and update its status to CLOSED
        loan = Loan.query.get(repayment.loan_id)
        if loan:
            repays = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == loan.loan_id).all()
            if repays and all((r.id == repayment.id or r.status == Status_Repayment.PAID) for r in repays):
                loan.status = Status_Loan.CLOSED

        db.session.commit()
        return jsonify({'message': 'success'})

    req = {
        'modal_amount_due': repayment.amount_due,
        'modal_repay_amount': repayment.amount_paid,
        'modal_pay_date': date.today().isoformat()
    }
    return jsonify(req)