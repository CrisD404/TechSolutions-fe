# TechSolutions - Frontend

Front simple desarrollado con **Python + Flask** y estilado con **Bootstrap**. Incluye dos
vistas (login y home), validación básica de email, sesión vía cookies y un servicio de login
mockeado que simula la respuesta de un backend.

## Requisitos

- Python 3.10 o superior

## Cómo levantar el proyecto

1. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Levantar la aplicación:

   ```bash
   python run.py
   ```

3. Abrir el navegador en:

   ```
   http://127.0.0.1:5000/
   ```

## Credenciales de prueba

El login está mockeado. Usá estas credenciales para ingresar:

- **Email:** `test@techsolutions.com`
- **Contraseña:** `123456`

Cualquier otra combinación devuelve un error de credenciales inválidas.

## Estructura del proyecto

```
TechSolutions-fe/
├── run.py                  # Punto de entrada
├── requirements.txt        # Dependencias
└── app/
    ├── __init__.py         # Application factory + manejo de errores
    ├── config.py           # Configuración (clave secreta, cookies)
    ├── auth/               # Login, logout, validación y servicio mock
    ├── main/               # Vista home (protegida)
    ├── templates/          # Plantillas HTML (base, login, home)
    └── static/             # CSS
```
