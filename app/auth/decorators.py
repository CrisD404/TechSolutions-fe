import time
from functools import wraps

from flask import abort, current_app, request, session


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        exp_cookie = request.cookies.get(current_app.config["AUTH_EXP_COOKIE"])

        try:
            exp_valid = exp_cookie is not None and int(exp_cookie) > time.time()
        except ValueError:
            exp_valid = False

        if not (session.get("logged_in") and exp_valid):
            session.clear()
            abort(401)

        return view_func(*args, **kwargs)

    return wrapped
