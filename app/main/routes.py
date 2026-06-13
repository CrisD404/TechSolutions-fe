from flask import Blueprint, render_template, session

from app.auth.decorators import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def home():
    user = session.get("user", {})
    return render_template("home.html", user=user)
