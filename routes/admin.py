from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request

admin = Blueprint("admin", __name__, url_prefix="/")


@admin.route("/admin/dashboard", methods=['GET'])
def dashboard():
    overdue_loan = [
        {
            'name': 'Hak Korlimhuor',
            'loan_id': 'LOAN_1',
            'inst': 6,
            'due_date': '2025-02-01',
            'amount_due': 889.50,
            'amount_paid': 333.09,
        }
    ]

    stat_data = {
        'customers': 12,
        'active_loans': 5,
        'total_disbursed': 45000.00,
        'total_collected': 18500.00,
        'monthly_labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        'monthly_disbursed': [5000, 8000, 12000, 6000, 9000, 15000, 10000],
        'monthly_collected': [3000, 4500, 7500, 5000, 7000, 12000, 8500],
        'status_counts': {'Pending': 3, 'Active': 5, 'Closed': 4}
    }

    if 'admin' not in session.get('role', ''):
        return redirect(url_for('root'))
    return render_template("admin/dashboard.html",
                           overdue_loan=overdue_loan,
                           stat_data=stat_data)


@admin.route("/admin/borrower", methods=['GET'])
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

    if session.get('user') is None:
        return redirect(url_for('root'))

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
def add_borrower():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/borrower/add.html")


@admin.route("/admin/borrower/view", methods=['GET'])
def view_borrower():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/borrower/view.html")


@admin.route("/admin/borrower/update", methods=['GET'])
def update_borrower():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/borrower/edit.html")


@admin.route("/admin/borrower/delete", methods=['GET', 'POST'])
def delete_borrower():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/borrower/borrower.html")


@admin.route("/admin/loan", methods=['GET'])
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

    if session.get('user') is None:
        return redirect(url_for('root'))



    return render_template("admin/loan/loan.html",
                           list=loan_list)


@admin.route("/admin/loan/view", methods=['GET'])
def view_loan():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/loan/view.html")


@admin.route("/admin/loan/add", methods=['GET', 'POST'])
def add_loan():
    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/loan/add.html")


@admin.route("/admin/loan/delete", methods=['GET', 'POST'])
def delete_loan():
    if session.get('user') is None:
        return redirect(url_for('root'))

    return render_template("admin/loan/loan.html")


@admin.route("/admin/report", methods=['GET'])
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

    if session.get('user') is None:
        return redirect(url_for('root'))
    return render_template("admin/report.html", list=loan_records_list)
