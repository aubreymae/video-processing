from flask import Flask

UPLOAD_FOLDER = "app/uploads"

def create_app():
    from app.api import bp as api_bp

    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.register_blueprint(api_bp, url_prefix="/api")

    return app