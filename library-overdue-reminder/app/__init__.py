from flask import Flask
from .config import load_config
from .database import db, init_db
from .routes import bp as api_bp
from .scheduler import init_scheduler
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    load_config(app)
    CORS(app)

    db.init_app(app)
    with app.app_context():
        init_db()

    app.register_blueprint(api_bp)
    init_scheduler(app)
    return app
