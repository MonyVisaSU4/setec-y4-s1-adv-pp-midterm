from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from flask_login import login_required

from decorators import admin_required
from extension import db
from models import Loan

admin = Blueprint("admin", __name__, url_prefix="/")



@admin.route("/admin/dashboard", methods=['GET'])
@admin_required
@login_required
def dashboard():
    query = db.select(Loan)
    total_borrower = db.session.scalar(query)
    print(f"Total Borrower: ${total_borrower}")
    return render_template("admin/dashboard.html",
                           overdue_loan=None)


@admin.route("/admin/borrower", methods=['GET'])
@admin_required
@login_required
def borrower():
    res = [
        {
            'id': 1,
            'name': 'Touch Sovannita',
            'nationality': 'Khmer',
            'phone': '0973003645',
            'email': 'visazin128@gmail.com',
            'create_at': '2026-07-19',
        },
        {
            'id': 2,
            'name': 'Mony Visa',
            'nationality': 'Vietnamese',
            'phone': '0973003645',
            'email': 'sovannita128@gmail.com',
            'create_at': '2026-07-19',
        }
    ]

    

    param = request.args.get('filter')

    if param is not None:
        query = param.strip().lower()
        if query:
            result = [r for r in res if query in r['name'].strip().lower() or query in r['nationality'].strip().lower()]
        else: result = res
        return jsonify(result)

    return render_template("admin/borrower/borrower.html",
                           list=res)

@admin.route("/admin/borrower/add", methods=['GET', 'POST'])
@login_required
@admin_required
def add_borrower():
    return render_template("admin/borrower/add.html")


@admin.route("/admin/borrower/view", methods=['GET'])
@login_required
@admin_required
def view_borrower():
    return render_template("admin/borrower/view.html")


@admin.route("/admin/borrower/update", methods=['GET'])
@login_required
@admin_required
def update_borrower():
    return render_template("admin/borrower/edit.html")


@admin.route("/admin/borrower/delete", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_borrower():
    
    return render_template("admin/borrower/borrower.html")


@admin.route("/admin/loan", methods=['GET'])
@login_required
@admin_required
def loan():
    loan_list = [
        {
            'id': '882',
            'borrower': 'Touch Sovannita',
            'principle': 5000.00,
            'rate': 8,
            'tenure': 9,
            'total_repayable': 5200.00,
            'status': 'pending',
            'start_date': '07/18/2026'
        },
        {
            'id': '884',
            'borrower': 'Hak Korlimhuor',
            'principle': 12000.00,
            'rate': 8,
            'tenure': 3,
            'total_repayable': 12200.00,
            'status': 'active',
            'start_date': '07/19/2026'
        }
    ]

    



    return render_template("admin/loan/loan.html",
                           list=loan_list)


@admin.route("/admin/loan/view", methods=['GET'])
@login_required
@admin_required
def view_loan():
    
    return render_template("admin/loan/view.html")


@admin.route("/admin/loan/add", methods=['GET', 'POST'])
@login_required
@admin_required
def add_loan():
    
    return render_template("admin/loan/add.html")


@admin.route("/admin/loan/delete", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_loan():
    

    return render_template("admin/loan/loan.html")


@admin.route("/admin/report", methods=['GET'])
@login_required
@admin_required
def report():
    loan_records_list = [
        {
            'name': 'Peang Leanghour',
            'principal': 5000.00,
            'rate': 8,
            'tenure': 2,
            'total_repayable': 45000.00,
            'status': 'Pending',
            'start_date': '07/19/2026'
        }
    ]

    
    return render_template("admin/report.html", list=loan_records_list)
