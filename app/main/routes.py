from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.auth.decorators import login_required
from app.main.mock_service import (
    REQUEST_AREAS,
    create_request,
    get_active_plan,
    get_all_requests,
    get_messages,
    get_notifications,
    get_plan_history,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def home():
    user = session.get("user", {})

    active_plan = get_active_plan()["data"]
    plan_history = get_plan_history()["data"]
    messages = get_messages()["data"]
    notifications = get_notifications()["data"]
    requests_list = get_all_requests()["data"]

    unread_messages = sum(1 for m in messages if not m["read"])
    unread_notifications = sum(1 for n in notifications if not n["read"])

    return render_template(
        "dashboard.html",
        user=user,
        active_plan=active_plan,
        plan_history=plan_history,
        messages=messages,
        notifications=notifications,
        requests_list=requests_list,
        areas=REQUEST_AREAS,
        unread_messages=unread_messages,
        unread_notifications=unread_notifications,
    )


@main_bp.route("/requests", methods=["POST"])
@login_required
def new_request():
    subject = request.form.get("subject", "").strip()
    area = request.form.get("area", "").strip()
    description = request.form.get("description", "").strip()

    if not subject or not area or not description:
        flash("Todos los campos son obligatorios.")
        return redirect(url_for("main.home"))

    response = create_request(subject, description, area)
    flash(response["message"])
    return redirect(url_for("main.home"))
