from flask import Flask, redirect, url_for, flash

from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.errorhandler(401)
    def unauthorized(_error):
        flash("Tu sesion no es valida o expiro. Por favor, ingresa nuevamente.")
        return redirect(url_for("auth.login"))

    return app
