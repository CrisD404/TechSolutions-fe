from datetime import datetime

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


def get_active_plan():
    # El cliente solo puede tener un plan vigente a la vez.
    return {
        "status_code": 200,
        "path": "/api/plans/active",
        "data": {
            "id": 2,
            "name": "Plan Profesional",
            "status": "active",
            "services": [
                {"name": "Soporte IT 24/7", "description": "Asistencia tecnica sin restriccion horaria"},
                {"name": "Consultoria Cloud", "description": "Migracion y optimizacion AWS/Azure"},
                {"name": "Seguridad avanzada", "description": "Auditorias, pentesting y monitoreo"},
                {"name": "Backup diario", "description": "Respaldo automatico con retencion 30 dias"},
            ],
            "start_date": "01/03/2026",
            "end_date": "28/02/2027",
        },
    }


def get_plan_history():
    # Planes anteriores ya finalizados (solo para consulta).
    return {
        "status_code": 200,
        "path": "/api/plans/history",
        "data": [
            {
                "id": 1,
                "name": "Plan Starter",
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
# Tipos de evento: created | modified | comment | status_change | resolved
_requests = [
    {
        "id": 1042,
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
            data.append({
                "id": f"req-{req['id']}",
                "type": "info",
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
    new_id = 1043 + len(_requests)
    now = datetime.now().strftime("%H:%M")
    new_request = {
        "id": new_id,
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
