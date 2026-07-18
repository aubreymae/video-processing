from flask import Flask

UPLOAD_FOLDER = "app/uploads"

app = Flask(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes