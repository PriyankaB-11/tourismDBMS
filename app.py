from flask import Flask, redirect, url_for
from config import Config
from db import close_db
from routes.auth import auth_bp
from routes.booking import booking_bp
from routes.destinations import destinations_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    import os
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(booking_bp)

    app.teardown_appcontext(close_db)

    @app.route("/")
    def home_redirect():
        return redirect(url_for("destinations.index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
