from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from config import Config
from extension import db, migrate
from login_manager import login_manager
from models import User
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
