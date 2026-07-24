from flask import Flask, render_template, request, redirect, url_for, session, make_response
from config import Config
from extension import db, migrate
from routes.admin import admin
from routes.customer import customer

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(admin)
app.register_blueprint(customer)

with app.app_context():
    db.create_all()
    migrate.init_app(app, db)

@app.route("/", methods=['GET', 'POST'])
def root():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'visa' and password == '123':
            session['user'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin.dashboard'))
        elif username == 'sota' and password == '123':
            session['user'] = username
            session['role'] = 'customer'
            return redirect(url_for('customer.dashboard'))
        else:
            error = "wrong username and password !!"

    return render_template('auth/login.html',
                           error=error)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.run(debug=True)
