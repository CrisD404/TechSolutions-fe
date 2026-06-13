from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.auth.mock_service import mock_login
from app.auth.validators import validate_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        remember = "remember" in request.form

        if not validate_email(email):
            flash("Ingresa un email valido.")
            return render_template("login.html")

        # Simulamos una llamada a un servicio de autenticación externo, quitar mock cuando el servicio esté listo
        response = mock_login(email, password, remember)

        if response["status_code"] == 200:
            data = response["data"]
            session["logged_in"] = True
            session["user"] = data["user"]

            max_age = (
                current_app.config["REMEMBER_MAX_AGE"]
                if remember
                else current_app.config["DEFAULT_MAX_AGE"]
            )

            resp = redirect(url_for("main.home"))
            resp.set_cookie(
                current_app.config["AUTH_TOKEN_COOKIE"],
                data["token"],
                max_age=max_age,
                httponly=True,
            )
            resp.set_cookie(
                current_app.config["AUTH_EXP_COOKIE"],
                str(data["exp"]),
                max_age=max_age,
                httponly=True,
            )
            return resp

        flash(response.get("message", "No se pudo iniciar sesion."))

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    resp = redirect(url_for("auth.login"))
    resp.delete_cookie(current_app.config["AUTH_TOKEN_COOKIE"])
    resp.delete_cookie(current_app.config["AUTH_EXP_COOKIE"])
    return resp
