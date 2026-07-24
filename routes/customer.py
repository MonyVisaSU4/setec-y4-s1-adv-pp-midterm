from flask import Blueprint, render_template, session, redirect, url_for

customer = Blueprint("customer", __name__, url_prefix="/")

@customer.route("/customer/dashboard", methods=['GET'])
def dashboard():
    lists = [
        {
            'principle': 12000.00,
            'interest_rate': 5,
            'duration': 1,
            'total_repayable': 25000.00,
            'total_paid': 6000.00,
            'status': 'pending',
            'start_date': '2026-04-09'
        }
    ]

    if 'customer' not in session['role']:
        return redirect(url_for('root'))
    return render_template("customer/dashboard.html", list=lists)

@customer.route("/customer/loan", methods=['GET'])
def loan():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("customer/loan.html")

@customer.route("/customer/profile", methods=['GET'])
def profile():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("customer/profile.html")

@customer.route("/customer/loan/schedule", methods=['GET'])
def schedule():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("customer/schedule.html")