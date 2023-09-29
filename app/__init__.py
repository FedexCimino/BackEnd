from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Migrate
from flask import CORS
from app.auth_routes import auth_bp
from app.api_routes import api_bp


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)  # Configura CORS para permitir solicitudes desde el frontend

from app import routes, models


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

