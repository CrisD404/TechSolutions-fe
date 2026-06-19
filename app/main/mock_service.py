from datetime import datetime, timedelta

REQUEST_AREAS = [
    "Soporte IT",
    "Cloud",
    "Seguridad",
    "Redes",
    "Consultoria",
    "Desarrollo",
    "Infraestructura",
    "Capacitacion",
]


# ===== Catalogo de planes (3 niveles) =====
PLANS_CATALOG = [
    {
        "id": "basico",
        "level": 1,
        "name": "Plan Basico",
        "tagline": "Para arrancar con lo esencial",
        "price": "USD 199/mes",
        "services": [
            {"name": "Soporte IT remoto", "description": "Asistencia tecnica L-V 9 a 18hs"},
            {"name": "Monitoreo basico", "description": "Alertas de caida de servicios"},
            {"name": "Backup semanal", "description": "Respaldo de datos criticos"},
        ],
    },
    {
        "id": "profesional",
        "level": 2,
        "name": "Plan Profesional",
        "tagline": "Para equipos en crecimiento",
        "price": "USD 499/mes",
        "services": [
            {"name": "Soporte IT 24/7", "description": "Asistencia tecnica sin restriccion horaria"},
            {"name": "Consultoria Cloud", "description": "Migracion y optimizacion AWS/Azure"},
            {"name": "Seguridad avanzada", "description": "Auditorias, pentesting y monitoreo"},
            {"name": "Backup diario", "description": "Respaldo automatico con retencion 30 dias"},
        ],
    },
    {
        "id": "premium",
        "level": 3,
        "name": "Plan Premium",
        "tagline": "Maximo nivel de servicio y respaldo",
        "price": "USD 999/mes",
        "services": [
            {"name": "Soporte IT 24/7 prioritario", "description": "Tiempos de respuesta garantizados"},
            {"name": "Consultor dedicado", "description": "Account manager asignado a tu cuenta"},
            {"name": "SLA 99.9%", "description": "Nivel de servicio garantizado por contrato"},
            {"name": "Seguridad gestionada", "description": "Auditorias trimestrales y respuesta a incidentes"},
            {"name": "DRP y backup en tiempo real", "description": "Plan de recuperacion ante desastres"},
        ],
    },
]


def _catalog_by_level(level):
    return next((p for p in PLANS_CATALOG if p["level"] == level), None)


def _catalog_by_id(plan_id):
    return next((p for p in PLANS_CATALOG if p["id"] == plan_id), None)


def _build_active_plan(level, start_date, end_date):
    plan = dict(_catalog_by_level(level))
    plan["status"] = "active"
    plan["start_date"] = start_date
    plan["end_date"] = end_date
    return plan


# Plan vigente del cliente (uno solo). Se actualiza al aprobarse un upgrade.
_active_plan = _build_active_plan(2, "01/03/2026", "28/02/2027")


def get_active_plan():
    return {"status_code": 200, "path": "/api/plans/active", "data": _active_plan}


def get_available_upgrades():
    # Solo los planes de nivel superior al plan activo.
    upgrades = [dict(p) for p in PLANS_CATALOG if p["level"] > _active_plan["level"]]
    return {"status_code": 200, "path": "/api/plans/upgrades", "data": upgrades}


def get_plan_history():
    # Planes anteriores ya finalizados (solo para consulta).
    return {
        "status_code": 200,
        "path": "/api/plans/history",
        "data": [
            {
                "id": 1,
                "name": "Plan Basico",
                "status": "expired",
                "start_date": "15/01/2025",
                "end_date": "28/02/2026",
            },
        ],
    }


def get_messages():
    return {
        "status_code": 200,
        "path": "/api/messages",
        "data": [
            {
                "id": 1,
                "from": "Soporte TechSolutions",
                "subject": "Mantenimiento programado",
                "preview": "El proximo sabado realizaremos tareas de mantenimiento...",
                "date": "19/06/2026",
                "read": False,
            },
            {
                "id": 2,
                "from": "Carlos Mendez",
                "subject": "Re: Consulta sobre migracion",
                "preview": "Adjunto el informe de relevamiento solicitado...",
                "date": "18/06/2026",
                "read": False,
            },
            {
                "id": 3,
                "from": "Facturacion",
                "subject": "Factura Junio 2026",
                "preview": "Se encuentra disponible tu factura del periodo...",
                "date": "15/06/2026",
                "read": True,
            },
        ],
    }


# ===== Solicitudes =====
# Almacen in-memory: cada solicitud persiste su timeline de eventos (NotiSys).
# kind: consulta | upgrade
# Tipos de evento: created | modified | comment | status_change | resolved | rejected
_requests = [
    {
        "id": 1042,
        "kind": "consulta",
        "subject": "Migracion base de datos a AWS",
        "area": "Cloud",
        "description": "Necesitamos migrar la base de datos productiva a AWS RDS minimizando el downtime.",
        "status": "en_progreso",
        "priority": "alta",
        "created": "10/06/2026",
        "assigned_to": "Carlos Mendez",
        "has_update": True,
        "last_update": "19/06/2026 09:00",
        "timeline": [
            {
                "type": "created",
                "title": "Solicitud creada",
                "description": "El cliente registro la solicitud.",
                "author": "Vos",
                "datetime": "10/06/2026 09:15",
            },
            {
                "type": "modified",
                "title": "Solicitud aprobada y asignada",
                "description": "La solicitud fue aprobada y asignada a Carlos Mendez.",
                "author": "TechSolutions",
                "datetime": "11/06/2026 10:00",
            },
            {
                "type": "comment",
                "title": "Respuesta del consultor",
                "description": "Iniciamos el relevamiento de la base actual y su volumen de datos.",
                "author": "Carlos Mendez",
                "datetime": "12/06/2026 16:30",
            },
            {
                "type": "status_change",
                "title": "Cambio de estado",
                "description": "Estado actualizado de Pendiente a En progreso.",
                "author": "Carlos Mendez",
                "datetime": "14/06/2026 11:00",
            },
            {
                "type": "comment",
                "title": "Respuesta del consultor",
                "description": "Avance: configuramos el entorno destino en AWS RDS y validamos la conectividad.",
                "author": "Carlos Mendez",
                "datetime": "19/06/2026 09:00",
            },
        ],
    },
    {
        "id": 1038,
        "kind": "consulta",
        "subject": "Configuracion VPN corporativa",
        "area": "Redes",
        "description": "Solicitamos configurar acceso VPN para el equipo remoto.",
        "status": "pendiente",
        "priority": "media",
        "created": "05/06/2026",
        "assigned_to": None,
        "has_update": False,
        "last_update": "06/06/2026 09:30",
        "timeline": [
            {
                "type": "created",
                "title": "Solicitud creada",
                "description": "El cliente registro la solicitud.",
                "author": "Vos",
                "datetime": "05/06/2026 14:20",
            },
            {
                "type": "comment",
                "title": "Respuesta del consultor",
                "description": "Recibimos tu solicitud, sera asignada a un consultor en breve.",
                "author": "Soporte TechSolutions",
                "datetime": "06/06/2026 09:30",
            },
        ],
    },
    {
        "id": 1035,
        "kind": "consulta",
        "subject": "Auditoria de seguridad web",
        "area": "Seguridad",
        "description": "Auditoria de seguridad sobre el portal de clientes.",
        "status": "completada",
        "priority": "alta",
        "created": "28/05/2026",
        "assigned_to": "Laura Gomez",
        "has_update": False,
        "last_update": "04/06/2026 17:30",
        "timeline": [
            {
                "type": "created",
                "title": "Solicitud creada",
                "description": "El cliente registro la solicitud.",
                "author": "Vos",
                "datetime": "28/05/2026 08:45",
            },
            {
                "type": "modified",
                "title": "Solicitud aprobada y asignada",
                "description": "La solicitud fue aprobada y asignada a Laura Gomez.",
                "author": "TechSolutions",
                "datetime": "29/05/2026 10:00",
            },
            {
                "type": "status_change",
                "title": "Cambio de estado",
                "description": "Estado actualizado de Pendiente a En progreso.",
                "author": "Laura Gomez",
                "datetime": "30/05/2026 15:00",
            },
            {
                "type": "comment",
                "title": "Respuesta del consultor",
                "description": "Detectamos 3 vulnerabilidades medias, adjuntamos el informe con recomendaciones.",
                "author": "Laura Gomez",
                "datetime": "02/06/2026 12:00",
            },
            {
                "type": "resolved",
                "title": "Solicitud resuelta",
                "description": "Auditoria finalizada y reporte entregado. Solicitud cerrada.",
                "author": "Laura Gomez",
                "datetime": "04/06/2026 17:30",
            },
        ],
    },
]


def _next_request_id():
    return max((r["id"] for r in _requests), default=1042) + 1


def get_all_requests():
    return {
        "status_code": 200,
        "path": "/api/requests",
        "data": _requests,
    }


def get_request(request_id):
    request = next((r for r in _requests if r["id"] == request_id), None)
    if request is None:
        return {"status_code": 404, "path": f"/api/requests/{request_id}", "data": None}
    return {"status_code": 200, "path": f"/api/requests/{request_id}", "data": request}


def mark_request_seen(request_id):
    request = next((r for r in _requests if r["id"] == request_id), None)
    if request is not None:
        request["has_update"] = False
    return request


def get_notifications():
    # Las notificaciones de actividad se derivan de las solicitudes con
    # actualizaciones no vistas, conectando la tabla con el icono del header.
    data = []
    for req in _requests:
        if req["has_update"]:
            last_event = req["timeline"][-1]
            etype = last_event["type"]
            ntype = "success" if etype == "resolved" else "warning" if etype == "rejected" else "info"
            data.append({
                "id": f"req-{req['id']}",
                "type": ntype,
                "message": f"Solicitud #{req['id']}: {last_event['title'].lower()}",
                "date": req["last_update"],
                "read": False,
                "request_id": req["id"],
            })

    # Notificacion general del sistema (no asociada a una solicitud).
    data.append({
        "id": "sys-plan",
        "type": "warning",
        "message": "Tu plan vence el 28/02/2027",
        "date": "18/06/2026",
        "read": True,
        "request_id": None,
    })

    return {"status_code": 200, "path": "/api/notifications", "data": data}


def create_request(subject, description, area):
    new_id = _next_request_id()
    now = datetime.now().strftime("%H:%M")
    new_request = {
        "id": new_id,
        "kind": "consulta",
        "subject": subject,
        "area": area,
        "description": description,
        "status": "pendiente",
        "priority": "media",
        "created": "19/06/2026",
        "assigned_to": None,
        "has_update": True,
        "last_update": f"19/06/2026 {now}",
        "timeline": [
            {
                "type": "created",
                "title": "Solicitud creada",
                "description": "El cliente registro la solicitud. Pendiente de asignacion.",
                "author": "Vos",
                "datetime": f"19/06/2026 {now}",
            },
        ],
    }
    _requests.insert(0, new_request)
    return {
        "status_code": 201,
        "path": "/api/requests",
        "data": new_request,
        "message": f"Solicitud #{new_id} creada exitosamente",
    }


# ===== Solicitudes de upgrade de plan =====
def get_pending_upgrade():
    return next(
        (r for r in _requests if r.get("kind") == "upgrade" and r["status"] == "pendiente"),
        None,
    )


def has_pending_upgrade():
    return get_pending_upgrade() is not None


def create_upgrade_request(target_plan_id, reason):
    target = _catalog_by_id(target_plan_id)
    if target is None or target["level"] <= _active_plan["level"]:
        return {
            "status_code": 400,
            "path": "/api/plans/upgrade",
            "data": None,
            "message": "El plan seleccionado no es un upgrade valido.",
        }

    # Bloqueo de solicitudes duplicadas.
    if has_pending_upgrade():
        return {
            "status_code": 409,
            "path": "/api/plans/upgrade",
            "data": None,
            "message": "Ya tenes una solicitud de upgrade en curso. Espera a que se resuelva.",
        }

    new_id = _next_request_id()
    now = datetime.now()
    stamp = now.strftime("%d/%m/%Y %H:%M")
    from_name = _active_plan["name"]
    to_name = target["name"]

    upgrade = {
        "id": new_id,
        "kind": "upgrade",
        "subject": f"Cambio de plan: {from_name} → {to_name}",
        "area": "Planes",
        "description": reason or "Sin motivo especificado.",
        "from_plan": from_name,
        "to_plan": to_name,
        "to_level": target["level"],
        "status": "pendiente",
        "priority": "media",
        "created": now.strftime("%d/%m/%Y"),
        "assigned_to": "Administracion",
        "has_update": False,
        "last_update": stamp,
        "timeline": [
            {
                "type": "created",
                "title": "Solicitud de upgrade enviada",
                "description": f"Solicitaste el cambio de {from_name} a {to_name}. Pendiente de aprobacion del administrador.",
                "author": "Vos",
                "datetime": stamp,
            },
        ],
    }
    _requests.insert(0, upgrade)
    return {
        "status_code": 201,
        "path": "/api/plans/upgrade",
        "data": upgrade,
        "message": f"Solicitud de upgrade #{new_id} enviada. Queda pendiente de aprobacion.",
    }


def resolve_upgrade(request_id, approved):
    """Simula la decision del administrador sobre una solicitud de upgrade."""
    global _active_plan

    req = next(
        (r for r in _requests if r["id"] == request_id and r.get("kind") == "upgrade"),
        None,
    )
    if req is None:
        return {
            "status_code": 404,
            "path": f"/api/plans/upgrade/{request_id}",
            "data": None,
            "message": "Solicitud de upgrade no encontrada.",
        }
    if req["status"] != "pendiente":
        return {
            "status_code": 409,
            "path": f"/api/plans/upgrade/{request_id}",
            "data": req,
            "message": "Esta solicitud ya fue resuelta.",
        }

    now = datetime.now()
    stamp = now.strftime("%d/%m/%Y %H:%M")

    if approved:
        req["status"] = "aprobada"
        req["timeline"].append({
            "type": "resolved",
            "title": "Upgrade aprobado",
            "description": "La solicitud fue aprobada por administracion. Se genero la facturacion del nuevo plan y tu plan activo fue actualizado automaticamente.",
            "author": "Administracion",
            "datetime": stamp,
        })
        start = now.strftime("%d/%m/%Y")
        end = (now + timedelta(days=365)).strftime("%d/%m/%Y")
        _active_plan = _build_active_plan(req["to_level"], start, end)
        message = f"Upgrade #{request_id} aprobado. Tu plan ahora es {req['to_plan']}."
    else:
        req["status"] = "rechazada"
        req["timeline"].append({
            "type": "rejected",
            "title": "Upgrade rechazado",
            "description": "La solicitud fue rechazada por administracion. Tu plan actual se mantiene sin cambios.",
            "author": "Administracion",
            "datetime": stamp,
        })
        message = f"Upgrade #{request_id} rechazado. Tu plan actual se mantiene."

    req["has_update"] = True
    req["last_update"] = stamp
    return {
        "status_code": 200,
        "path": f"/api/plans/upgrade/{request_id}",
        "data": req,
        "message": message,
    }
