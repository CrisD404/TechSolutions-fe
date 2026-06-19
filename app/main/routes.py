from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.auth.decorators import login_required
from app.main.mock_service import (
    REQUEST_AREAS,
    create_request,
    create_upgrade_request,
    get_active_plan,
    get_all_requests,
    get_available_upgrades,
    get_messages,
    get_notifications,
    get_pending_upgrade,
    get_plan_history,
    get_request,
    mark_request_seen,
    resolve_upgrade,
)

main_bp = Blueprint("main", __name__)


def _navbar_context():
    """Datos compartidos por todas las vistas que muestran el navbar."""
    messages = get_messages()["data"]
    notifications = get_notifications()["data"]
    return {
        "user": session.get("user", {}),
        "messages": messages,
        "notifications": notifications,
        "unread_messages": sum(1 for m in messages if not m["read"]),
        "unread_notifications": sum(1 for n in notifications if not n["read"]),
    }


@main_bp.route("/")
@login_required
def home():
    active_plan = get_active_plan()["data"]
    plan_history = get_plan_history()["data"]
    requests_list = get_all_requests()["data"]
    pending_upgrade = get_pending_upgrade()

    return render_template(
        "dashboard.html",
        active_plan=active_plan,
        plan_history=plan_history,
        requests_list=requests_list,
        areas=REQUEST_AREAS,
        can_upgrade=len(get_available_upgrades()["data"]) > 0,
        pending_upgrade=pending_upgrade,
        **_navbar_context(),
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


@main_bp.route("/requests/<int:request_id>")
@login_required
def request_detail(request_id):
    response = get_request(request_id)
    if response["status_code"] == 404:
        flash("La solicitud solicitada no existe.")
        return redirect(url_for("main.home"))

    # Al abrir el detalle, las actualizaciones quedan marcadas como vistas.
    mark_request_seen(request_id)

    return render_template(
        "request_detail.html",
        request_item=response["data"],
        **_navbar_context(),
    )


@main_bp.route("/plans")
@login_required
def plans():
    pending_upgrade = get_pending_upgrade()
    return render_template(
        "plans.html",
        active_plan=get_active_plan()["data"],
        upgrades=get_available_upgrades()["data"],
        pending_upgrade=pending_upgrade,
        **_navbar_context(),
    )


@main_bp.route("/plans/upgrade", methods=["POST"])
@login_required
def request_upgrade():
    target_plan_id = request.form.get("target_plan_id", "").strip()
    reason = request.form.get("reason", "").strip()

    response = create_upgrade_request(target_plan_id, reason)
    flash(response["message"])

    if response["status_code"] == 201:
        return redirect(url_for("main.home"))
    return redirect(url_for("main.plans"))


@main_bp.route("/requests/<int:request_id>/resolve", methods=["POST"])
@login_required
def resolve_upgrade_view(request_id):
    # Simulacion de la decision del administrador (solo para demo).
    # Redirige al dashboard para que se vea la notificacion de resultado
    # y, si fue aprobada, el plan activo ya actualizado.
    decision = request.form.get("decision", "")
    response = resolve_upgrade(request_id, approved=(decision == "approve"))
    flash(response["message"])
    return redirect(url_for("main.home"))
