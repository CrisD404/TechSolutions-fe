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

_requests_store = []


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


def get_notifications():
    return {
        "status_code": 200,
        "path": "/api/notifications",
        "data": [
            {
                "id": 1,
                "type": "info",
                "message": "Tu solicitud #1042 fue asignada a un consultor",
                "date": "19/06/2026",
                "read": False,
            },
            {
                "id": 2,
                "type": "success",
                "message": "Backup completado exitosamente",
                "date": "19/06/2026",
                "read": False,
            },
            {
                "id": 3,
                "type": "warning",
                "message": "Tu plan Starter vence en 30 dias",
                "date": "18/06/2026",
                "read": True,
            },
        ],
    }


_REQUESTS_BASE = [
    {
        "id": 1042,
        "subject": "Migracion base de datos a AWS",
        "area": "Cloud",
        "status": "en_progreso",
        "priority": "alta",
        "created": "10/06/2026",
        "assigned_to": "Carlos Mendez",
    },
    {
        "id": 1038,
        "subject": "Configuracion VPN corporativa",
        "area": "Redes",
        "status": "pendiente",
        "priority": "media",
        "created": "05/06/2026",
        "assigned_to": None,
    },
    {
        "id": 1035,
        "subject": "Auditoria de seguridad web",
        "area": "Seguridad",
        "status": "completada",
        "priority": "alta",
        "created": "28/05/2026",
        "assigned_to": "Laura Gomez",
    },
]


def get_requests():
    return {
        "status_code": 200,
        "path": "/api/requests",
        "data": _REQUESTS_BASE,
    }


def get_all_requests():
    return {
        "status_code": 200,
        "path": "/api/requests",
        "data": _requests_store + _REQUESTS_BASE,
    }


def create_request(subject, description, area):
    new_id = 1050 + len(_requests_store)
    new_request = {
        "id": new_id,
        "subject": subject,
        "area": area,
        "description": description,
        "status": "pendiente",
        "priority": "media",
        "created": "19/06/2026",
        "assigned_to": None,
    }
    _requests_store.append(new_request)
    return {
        "status_code": 201,
        "path": "/api/requests",
        "data": new_request,
        "message": f"Solicitud #{new_id} creada exitosamente",
    }
