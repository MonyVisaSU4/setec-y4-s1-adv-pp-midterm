from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('root'))

        if current_user.role != "admin":
            return redirect(url_for('root'))
        return f(*args, **kwargs)

    return wrap
