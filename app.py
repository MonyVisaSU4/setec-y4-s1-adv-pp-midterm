from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from config import Config
from extension import db, migrate
from login_manager import login_manager
from models import User, RepaymentSchedule, Loan
from models.loan import Status as Status_Loan
from models.repayment_schedule import Status as Status_Repay
from routes.admin import admin
from routes.customer import customer

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "root"

app.register_blueprint(admin)
app.register_blueprint(customer)

with app.app_context():
    db.create_all()
    migrate.init_app(app, db)


def sync_status_overdue():
    with app.app_context():
        overdue_status = (
            db.session.query(RepaymentSchedule)
            .filter(
                RepaymentSchedule.due_date < date.today(),
                RepaymentSchedule._status != Status_Repay.PAID,
            ).update({
                RepaymentSchedule._status:
                    Status_Repay.OVERDUE
            }, synchronize_session=False)
        )
        db.session.commit()
        return overdue_status


def sync_closed_status():
    with app.app_context():
        loans = Loan.query.all()

        for l in loans:
            repays = RepaymentSchedule.query.filter(RepaymentSchedule.loan_id == l.loan_id).all()
            if repays and all(r.status == Status_Repay.PAID for r in repays):
                l.status = Status_Loan.CLOSED
        db.session.commit()


job_scheduler = BackgroundScheduler()
job_scheduler.add_job(sync_status_overdue, 'interval', hours=24)
job_scheduler.add_job(sync_closed_status, 'interval', hours=24)
job_scheduler.start()


@app.route("/", methods=['GET', 'POST'])
def root():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("customer.dashboard"))

    error = None

    if request.method == "POST":
        email: str = request.form.get("email")
        password: str = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.get_password(), password):
            login_user(user)

            print("Login called")
            print("Authenticated:", current_user.is_authenticated)
            print("User ID:", current_user.get_id())

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("customer.dashboard"))
        error = "Invalid email or password."

    return render_template('auth/login.html',
                           error=error)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('root'))


if __name__ == "__main__":
    app.run(debug=True)
