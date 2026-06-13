import time
import uuid

from flask import current_app

VALID_EMAIL = "test@techsolutions.com"
VALID_PASSWORD = "123456"


def mock_login(email: str, password: str, remember: bool) -> dict:
    """Simula la respuesta de un backend de autenticacion."""
    if email == VALID_EMAIL and password == VALID_PASSWORD:
        max_age = (
            current_app.config["REMEMBER_MAX_AGE"]
            if remember
            else current_app.config["DEFAULT_MAX_AGE"]
        )
        exp = int(time.time()) + max_age

        return {
            "status_code": 200,
            "path": "/api/login",
            "data": {
                "token": f"mocked-jwt-{uuid.uuid4().hex}",
                "exp": exp,
                "user": {
                    "id": 1,
                    "name": "Usuario de Prueba",
                    "email": email,
                },
            },
        }

    return {
        "status_code": 401,
        "path": "/api/login",
        "data": None,
        "message": "Credenciales invalidas",
    }
