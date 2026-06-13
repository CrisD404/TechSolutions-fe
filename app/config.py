class Config:
    SECRET_KEY = "dev-secret-key-change-in-production"

    AUTH_TOKEN_COOKIE = "token"
    AUTH_EXP_COOKIE = "exp"

    # Duracion de la sesion segun el checkbox "Recordarme"
    REMEMBER_MAX_AGE = 60 * 60 * 24 * 30  # 30 dias
    DEFAULT_MAX_AGE = 60 * 60 * 24  # 1 dia
